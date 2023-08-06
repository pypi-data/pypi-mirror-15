import pytz
import urlparse

from django.contrib.contenttypes.models import ContentType
from django.db import transaction
from django.template.defaultfilters import slugify
from django.utils import timezone
from netaddr import IPNetwork
from rest_framework import serializers, reverse
from taggit.models import Tag

from nodeconductor.core import models as core_models
from nodeconductor.core import serializers as core_serializers
from nodeconductor.core import utils as core_utils
from nodeconductor.core.fields import JsonField, MappedChoiceField
from nodeconductor.quotas import serializers as quotas_serializers
from nodeconductor.structure import serializers as structure_serializers

from . import models
from .backend import OpenStackBackendError


class ServiceSerializer(structure_serializers.BaseServiceSerializer):

    SERVICE_ACCOUNT_FIELDS = {
        'backend_url': 'Keystone auth URL (e.g. http://keystone.example.com:5000/v2.0)',
        'username': 'Administrative user',
        'password': '',
    }
    SERVICE_ACCOUNT_EXTRA_FIELDS = {
        'tenant_name': 'Administrative tenant (default: "admin")',
        'availability_zone': 'Default availability zone for provisioned Instances',
        'cpu_overcommit_ratio': '(default: 1)',
        'external_network_id': 'ID of OpenStack external network that will be connected to new service tenants',
        'coordinates': 'Coordianates of the datacenter, for example: {"latitude": 40.712784, "longitude": -74.005941}',
        'autocreate_tenants': 'Automatically create tenant for new SPL (default: False)',
    }

    class Meta(structure_serializers.BaseServiceSerializer.Meta):
        model = models.OpenStackService
        view_name = 'openstack-detail'


class FlavorSerializer(structure_serializers.BasePropertySerializer):

    class Meta(object):
        model = models.Flavor
        view_name = 'openstack-flavor-detail'
        fields = ('url', 'uuid', 'name', 'cores', 'ram', 'disk', 'display_name')
        extra_kwargs = {
            'url': {'lookup_field': 'uuid'},
        }

    display_name = serializers.SerializerMethodField()

    def get_display_name(self, flavor):
        return "{} ({} CPU, {} MB RAM, {} MB HDD)".format(
            flavor.name, flavor.cores, flavor.ram, flavor.disk)


class ImageSerializer(structure_serializers.BasePropertySerializer):

    class Meta(object):
        model = models.Image
        view_name = 'openstack-image-detail'
        fields = ('url', 'uuid', 'name', 'min_disk', 'min_ram')
        extra_kwargs = {
            'url': {'lookup_field': 'uuid'},
        }


class ServiceProjectLinkSerializer(structure_serializers.BaseServiceProjectLinkSerializer):

    state = serializers.SerializerMethodField()
    quotas = quotas_serializers.QuotaSerializer(many=True, read_only=True)

    def get_state(self, obj):
        if obj.tenant:
            return obj.tenant.human_readable_state
        return None

    class Meta(structure_serializers.BaseServiceProjectLinkSerializer.Meta):
        model = models.OpenStackServiceProjectLink
        view_name = 'openstack-spl-detail'
        fields = structure_serializers.BaseServiceProjectLinkSerializer.Meta.fields + (
            'quotas', 'tenant_id', 'external_network_id', 'internal_network_id', 'state'
        )
        extra_kwargs = {
            'service': {'lookup_field': 'uuid', 'view_name': 'openstack-detail'},
        }


class TenantQuotaSerializer(serializers.Serializer):
    instances = serializers.IntegerField(min_value=1, required=False)
    ram = serializers.IntegerField(min_value=1, required=False)
    vcpu = serializers.IntegerField(min_value=1, required=False)
    storage = serializers.IntegerField(min_value=1, required=False)
    security_group_count = serializers.IntegerField(min_value=1, required=False)
    security_group_rule_count = serializers.IntegerField(min_value=1, required=False)


class NestedServiceProjectLinkSerializer(structure_serializers.PermissionFieldFilteringMixin,
                                         core_serializers.AugmentedSerializerMixin,
                                         core_serializers.HyperlinkedRelatedModelSerializer):

    quotas = quotas_serializers.QuotaSerializer(many=True, read_only=True)

    class Meta(object):
        model = models.OpenStackServiceProjectLink
        fields = (
            'url',
            'project', 'project_name', 'project_uuid',
            'service', 'service_name', 'service_uuid',
            'quotas',
        )
        related_paths = 'project', 'service'
        view_name = 'openstack-spl-detail'
        extra_kwargs = {
            'service': {'lookup_field': 'uuid', 'view_name': 'openstack-detail'},
            'project': {'lookup_field': 'uuid'},
        }

    def run_validators(self, value):
        # No need to validate any fields except 'url' that is validated in to_internal_value method
        pass

    def get_filtered_field_names(self):
        return 'project', 'service'


class NestedSecurityGroupRuleSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.SecurityGroupRule
        fields = ('id', 'protocol', 'from_port', 'to_port', 'cidr')

    def to_internal_value(self, data):
        # Return exist security group as internal value if id is provided
        if 'id' in data:
            try:
                return models.SecurityGroupRule.objects.get(id=data['id'])
            except models.SecurityGroup:
                raise serializers.ValidationError('Security group with id %s does not exist' % data['id'])
        else:
            internal_data = super(NestedSecurityGroupRuleSerializer, self).to_internal_value(data)
            return models.SecurityGroupRule(**internal_data)


class ExternalNetworkSerializer(serializers.Serializer):
    vlan_id = serializers.CharField(required=False)
    vxlan_id = serializers.CharField(required=False)
    network_ip = core_serializers.IPAddressField()
    network_prefix = serializers.IntegerField(min_value=0, max_value=32)
    ips_count = serializers.IntegerField(min_value=1, required=False)

    def validate(self, attrs):
        vlan_id = attrs.get('vlan_id')
        vxlan_id = attrs.get('vxlan_id')

        if vlan_id is None and vxlan_id is None:
            raise serializers.ValidationError("VLAN or VXLAN ID should be provided.")
        elif vlan_id and vxlan_id:
            raise serializers.ValidationError("VLAN and VXLAN networks cannot be created simultaneously.")

        ips_count = attrs.get('ips_count')
        if ips_count is None:
            return attrs

        network_ip = attrs.get('network_ip')
        network_prefix = attrs.get('network_prefix')

        cidr = IPNetwork(network_ip)
        cidr.prefixlen = network_prefix

        # subtract router and broadcast IPs
        if cidr.size < ips_count - 2:
            raise serializers.ValidationError("Not enough Floating IP Addresses available.")

        return attrs


class AssignFloatingIpSerializer(serializers.Serializer):
    floating_ip = serializers.HyperlinkedRelatedField(
        label='Floating IP',
        required=True,
        view_name='openstack-fip-detail',
        lookup_field='uuid',
        queryset=models.FloatingIP.objects.all()
    )

    def get_fields(self):
        fields = super(AssignFloatingIpSerializer, self).get_fields()
        if self.instance:
            query_params = {
                'status': 'DOWN',
                'project': self.instance.service_project_link.project.uuid,
                'service': self.instance.service_project_link.service.uuid
            }

            field = fields['floating_ip']
            field.query_params = query_params
            field.value_field = 'url'
            field.display_name_field = 'address'
        return fields

    def get_floating_ip_uuid(self):
        return self.validated_data.get('floating_ip').uuid.hex

    def validate_floating_ip(self, value):
        if value is not None:
            if value.status == 'ACTIVE':
                raise serializers.ValidationError("Floating IP status must be DOWN.")
            elif value.service_project_link != self.instance.service_project_link:
                raise serializers.ValidationError("Floating IP must belong to same service project link.")
        return value

    def validate(self, attrs):
        if not self.instance.service_project_link.external_network_id:
            raise serializers.ValidationError(
                "External network ID of the service project link is missing.")
        elif self.instance.service_project_link.tenant.state != core_models.StateMixin.States.OK:
            raise serializers.ValidationError(
                "Service project link of instance should be in stable state.")

        return attrs


class FloatingIPSerializer(serializers.HyperlinkedModelSerializer):
    service_project_link = NestedServiceProjectLinkSerializer(read_only=True)

    class Meta:
        model = models.FloatingIP
        fields = ('url', 'uuid', 'status', 'address',
                  'service_project_link', 'backend_id', 'backend_network_id')
        extra_kwargs = {
            'url': {'lookup_field': 'uuid'},
        }
        view_name = 'openstack-fip-detail'


class SecurityGroupSerializer(core_serializers.AugmentedSerializerMixin,
                              structure_serializers.BasePropertySerializer):

    state = MappedChoiceField(
        choices=[(v, k) for k, v in core_models.StateMixin.States.CHOICES],
        choice_mappings={v: k for k, v in core_models.StateMixin.States.CHOICES},
        read_only=True,
    )
    rules = NestedSecurityGroupRuleSerializer(many=True)
    service_project_link = NestedServiceProjectLinkSerializer(
        queryset=models.OpenStackServiceProjectLink.objects.all())

    class Meta(object):
        model = models.SecurityGroup
        fields = ('url', 'uuid', 'state', 'name', 'description', 'rules', 'service_project_link')
        read_only_fields = ('url', 'uuid')
        extra_kwargs = {
            'url': {'lookup_field': 'uuid'},
            'service_project_link': {'view_name': 'openstack-spl-detail'}
        }
        view_name = 'openstack-sgp-detail'
        protected_fields = ('service_project_link',)

    def validate(self, attrs):
        if self.instance is None:
            # Check security groups quotas on creation
            service_project_link = attrs.get('service_project_link')
            security_group_count_quota = service_project_link.quotas.get(name='security_group_count')
            if security_group_count_quota.is_exceeded(delta=1):
                raise serializers.ValidationError('Can not create new security group - amount quota exceeded')
            security_group_rule_count_quota = service_project_link.quotas.get(name='security_group_rule_count')
            if security_group_rule_count_quota.is_exceeded(delta=len(attrs.get('rules', []))):
                raise serializers.ValidationError('Can not create new security group - rules amount quota exceeded')
        else:
            # Check security_groups quotas on update
            service_project_link = self.instance.service_project_link
            new_rules_count = len(attrs.get('rules', [])) - self.instance.rules.count()
            if new_rules_count > 0:
                security_group_rule_count_quota = service_project_link.quotas.get(name='security_group_rule_count')
                if security_group_rule_count_quota.is_exceeded(delta=new_rules_count):
                    raise serializers.ValidationError(
                        'Can not update new security group rules - rules amount quota exceeded')

        return attrs

    def validate_rules(self, value):
        for rule in value:
            rule.full_clean(exclude=['security_group'])
            if rule.id is not None and self.instance is None:
                raise serializers.ValidationError('Cannot add existed rule with id %s to new security group' % rule.id)
            elif rule.id is not None and self.instance is not None and rule.security_group != self.instance:
                raise serializers.ValidationError('Cannot add rule with id {} to group {} - it already belongs to '
                                                  'other group' % (rule.id, self.isntance.name))
        return value

    def create(self, validated_data):
        rules = validated_data.pop('rules', [])
        with transaction.atomic():
            security_group = super(SecurityGroupSerializer, self).create(validated_data)
            for rule in rules:
                security_group.rules.add(rule)

        return security_group

    def update(self, instance, validated_data):
        rules = validated_data.pop('rules', [])
        new_rules = [rule for rule in rules if rule.id is None]
        existed_rules = set([rule for rule in rules if rule.id is not None])

        security_group = super(SecurityGroupSerializer, self).update(instance, validated_data)
        old_rules = set(security_group.rules.all())

        with transaction.atomic():
            removed_rules = old_rules - existed_rules
            for rule in removed_rules:
                rule.delete()

            for rule in new_rules:
                security_group.rules.add(rule)

        return security_group


class InstanceSecurityGroupSerializer(serializers.ModelSerializer):

    name = serializers.ReadOnlyField(source='security_group.name')
    rules = NestedSecurityGroupRuleSerializer(
        source='security_group.rules',
        many=True,
        read_only=True,
    )
    url = serializers.HyperlinkedRelatedField(
        source='security_group',
        lookup_field='uuid',
        view_name='openstack-sgp-detail',
        queryset=models.SecurityGroup.objects.all(),
    )
    description = serializers.ReadOnlyField(source='security_group.description')

    class Meta(object):
        model = models.InstanceSecurityGroup
        fields = ('url', 'name', 'rules', 'description')
        extra_kwargs = {
            'url': {'lookup_field': 'uuid'},
        }
        view_name = 'openstack-sgp-detail'


class BackupScheduleSerializer(serializers.HyperlinkedModelSerializer):
    instance_name = serializers.ReadOnlyField(source='instance.name')
    timezone = serializers.ChoiceField(choices=[(t, t) for t in pytz.all_timezones],
                                       default=timezone.get_current_timezone_name)
    instance = serializers.HyperlinkedRelatedField(
        lookup_field='uuid',
        view_name='openstack-instance-detail',
        queryset=models.Instance.objects.all(),
    )

    class Meta(object):
        model = models.BackupSchedule
        view_name = 'openstack-schedule-detail'
        fields = ('url', 'uuid', 'description', 'backups', 'retention_time', 'timezone',
                  'instance', 'maximal_number_of_backups', 'schedule', 'is_active', 'instance_name')
        read_only_fields = ('is_active', 'backups')
        extra_kwargs = {
            'url': {'lookup_field': 'uuid'},
            'instance': {'lookup_field': 'uuid'},
            'backups': {'lookup_field': 'uuid'},
        }


class BackupSerializer(serializers.HyperlinkedModelSerializer):
    state = serializers.ReadOnlyField(source='get_state_display')
    metadata = JsonField(read_only=True)
    instance_name = serializers.ReadOnlyField(source='instance.name')
    instance = serializers.HyperlinkedRelatedField(
        lookup_field='uuid',
        view_name='openstack-instance-detail',
        queryset=models.Instance.objects.all(),
    )

    class Meta(object):
        model = models.Backup
        view_name = 'openstack-backup-detail'
        fields = ('url', 'uuid', 'description', 'created_at', 'kept_until', 'instance', 'state', 'backup_schedule',
                  'metadata', 'instance_name')
        read_only_fields = ('created_at', 'kept_until', 'backup_schedule')
        extra_kwargs = {
            'url': {'lookup_field': 'uuid'},
            'instance': {'lookup_field': 'uuid'},
            'backup_schedule': {'lookup_field': 'uuid'},
        }


class BackupRestorationSerializer(serializers.ModelSerializer):
    service_project_link = serializers.PrimaryKeyRelatedField(
        queryset=models.OpenStackServiceProjectLink.objects.all())

    flavor = serializers.HyperlinkedRelatedField(
        view_name='openstack-flavor-detail',
        lookup_field='uuid',
        queryset=models.Flavor.objects.all().select_related('settings'),
        write_only=True)

    system_volume_id = serializers.CharField(required=False)
    system_volume_size = serializers.IntegerField(required=False, min_value=0)
    data_volume_id = serializers.CharField(required=False)
    data_volume_size = serializers.IntegerField(required=False, min_value=0)

    class Meta(object):
        model = models.Instance
        fields = (
            'name', 'description',
            'service_project_link',
            'flavor', 'min_ram', 'min_disk',
            'key_name', 'key_fingerprint',
            'system_volume_id', 'system_volume_size',
            'data_volume_id', 'data_volume_size',
            'flavor_name', 'image_name',
            'user_data',
        )
        extra_kwargs = {
            'url': {'lookup_field': 'uuid'},
        }

    def validate(self, attrs):
        flavor = attrs['flavor']
        spl = attrs['service_project_link']

        if flavor.settings != spl.service.settings:
            raise serializers.ValidationError({'flavor': "Flavor is not within services' settings."})

        system_volume_size = attrs['system_volume_size']
        data_volume_size = attrs.get('data_volume_size', models.Instance.DEFAULT_DATA_VOLUME_SIZE)
        quota_usage = {
            'storage': system_volume_size + data_volume_size,
            'vcpu': flavor.cores,
            'ram': flavor.ram,
        }

        quota_errors = spl.validate_quota_change(quota_usage)
        if quota_errors:
            raise serializers.ValidationError(
                'One or more quotas are over limit: \n' + '\n'.join(quota_errors))

        return attrs


class InstanceSerializer(structure_serializers.VirtualMachineSerializer):

    service = serializers.HyperlinkedRelatedField(
        source='service_project_link.service',
        view_name='openstack-detail',
        read_only=True,
        lookup_field='uuid')

    service_project_link = serializers.HyperlinkedRelatedField(
        view_name='openstack-spl-detail',
        queryset=models.OpenStackServiceProjectLink.objects.all())

    flavor = serializers.HyperlinkedRelatedField(
        view_name='openstack-flavor-detail',
        lookup_field='uuid',
        queryset=models.Flavor.objects.all().select_related('settings'),
        write_only=True)

    image = serializers.HyperlinkedRelatedField(
        view_name='openstack-image-detail',
        lookup_field='uuid',
        queryset=models.Image.objects.all().select_related('settings'),
        write_only=True)

    security_groups = InstanceSecurityGroupSerializer(
        many=True, required=False, read_only=False)

    backups = BackupSerializer(many=True, read_only=True)
    backup_schedules = BackupScheduleSerializer(many=True, read_only=True)

    skip_external_ip_assignment = serializers.BooleanField(write_only=True, default=False)

    class Meta(structure_serializers.VirtualMachineSerializer.Meta):
        model = models.Instance
        view_name = 'openstack-instance-detail'
        fields = structure_serializers.VirtualMachineSerializer.Meta.fields + (
            'flavor', 'image', 'system_volume_size', 'data_volume_size', 'skip_external_ip_assignment',
            'security_groups', 'internal_ips', 'backups', 'backup_schedules', 'flavor_disk',
        )
        protected_fields = structure_serializers.VirtualMachineSerializer.Meta.protected_fields + (
            'flavor', 'image', 'system_volume_size', 'data_volume_size', 'skip_external_ip_assignment',
        )
        read_only_fields = structure_serializers.VirtualMachineSerializer.Meta.read_only_fields + ('flavor_disk',)

    def get_fields(self):
        fields = super(InstanceSerializer, self).get_fields()
        if 'system_volume_size' in fields:
            fields['system_volume_size'].required = True
        return fields

    def validate(self, attrs):
        # skip validation on object update
        if self.instance is not None:
            return attrs

        service_project_link = attrs['service_project_link']
        settings = service_project_link.service.settings
        flavor = attrs['flavor']
        image = attrs['image']

        floating_ip_count_quota = service_project_link.quotas.get(name='floating_ip_count')
        if floating_ip_count_quota.is_exceeded(delta=1):
            raise serializers.ValidationError({
                'service_project_link': 'Can not allocate floating IP - quota has been filled'}
            )

        if any([flavor.settings != settings, image.settings != settings]):
            raise serializers.ValidationError(
                "Flavor and image must belong to the same service settings as service project link.")

        if image.min_ram > flavor.ram:
            raise serializers.ValidationError(
                {'flavor': "RAM of flavor is not enough for selected image %s" % image.min_ram})

        if image.min_disk > attrs['system_volume_size']:
            raise serializers.ValidationError(
                {'system_volume_size': "System volume size has to be greater than %s" % image.min_disk})

        for security_group_data in attrs.get('security_groups', []):
            security_group = security_group_data['security_group']
            if security_group.service_project_link != attrs['service_project_link']:
                raise serializers.ValidationError(
                    "Security group {} has wrong service or project. New instance and its "
                    "security groups have to belong to same project and service".format(security_group.name))

        if not attrs['skip_external_ip_assignment']:
            options = settings.options or {}
            tenant = service_project_link.tenant
            if tenant is None:
                missed_net = 'external_network_id' not in options
            else:
                missed_net = tenant.state == core_models.StateMixin.States.OK and not tenant.external_network_id

            if missed_net:
                raise serializers.ValidationError(
                    "Cannot assign external IP if service project link has no external network")

        return attrs

    def create(self, validated_data):
        security_groups = [data['security_group'] for data in validated_data.pop('security_groups', [])]
        instance = super(InstanceSerializer, self).create(validated_data)

        for sg in security_groups:
            instance.security_groups.create(security_group=sg)

        return instance

    def update(self, instance, validated_data):
        security_groups = validated_data.pop('security_groups', [])
        security_groups = [data['security_group'] for data in security_groups]
        instance = super(InstanceSerializer, self).update(instance, validated_data)

        instance.security_groups.all().delete()
        for sg in security_groups:
            instance.security_groups.create(security_group=sg)

        return instance


class InstanceImportSerializer(structure_serializers.BaseResourceImportSerializer):

    class Meta(structure_serializers.BaseResourceImportSerializer.Meta):
        model = models.Instance
        view_name = 'openstack-instance-detail'

    def create(self, validated_data):
        spl = validated_data['service_project_link']
        backend = spl.get_backend()

        try:
            backend_instance = backend.get_instance(validated_data['backend_id'])
        except OpenStackBackendError as e:
            raise serializers.ValidationError(
                {'backend_id': "Can't import instance with ID %s. Reason: %s" % (validated_data['backend_id'], e)})

        backend_security_groups = backend_instance.nc_model_data.pop('security_groups')
        security_groups = spl.security_groups.filter(name__in=backend_security_groups)
        if security_groups.count() != len(backend_security_groups):
            raise serializers.ValidationError(
                {'backend_id': "Security groups for instance ID %s "
                               "are missed in NodeConductor" % validated_data['backend_id']})

        validated_data.update(backend_instance.nc_model_data)
        instance = super(InstanceImportSerializer, self).create(validated_data)

        for sg in security_groups:
            instance.security_groups.create(security_group=sg)

        return instance


class InstanceResizeSerializer(structure_serializers.PermissionFieldFilteringMixin,
                               serializers.Serializer):
    flavor = serializers.HyperlinkedRelatedField(
        view_name='openstack-flavor-detail',
        lookup_field='uuid',
        queryset=models.Flavor.objects.all(),
        required=False,
    )
    disk_size = serializers.IntegerField(min_value=1, required=False, label='Disk size')

    def get_fields(self):
        fields = super(InstanceResizeSerializer, self).get_fields()
        if self.instance:
            fields['disk_size'].min_value = self.instance.data_volume_size
            fields['flavor'].query_params = {
                'settings_uuid': self.instance.service_project_link.service.settings.uuid
            }
        return fields

    def get_filtered_field_names(self):
        return 'flavor',

    def validate_flavor(self, value):
        if value is not None:
            spl = self.instance.service_project_link

            if value.settings != spl.service.settings:
                raise serializers.ValidationError(
                    "New flavor is not within the same service settings")

            if value.disk < self.instance.flavor_disk:
                raise serializers.ValidationError("New flavor disk should be greater than the previous value.")

            quota_errors = spl.validate_quota_change({
                'vcpu': value.cores - self.instance.cores,
                'ram': value.ram - self.instance.ram,
            })
            if quota_errors:
                raise serializers.ValidationError(
                    "One or more quotas are over limit: \n" + "\n".join(quota_errors))
        return value

    def validate_disk_size(self, value):
        if value is not None:
            if value <= self.instance.data_volume_size:
                raise serializers.ValidationError(
                    "Disk size must be strictly greater than the current one")

            quota_errors = self.instance.service_project_link.validate_quota_change({
                'storage': value - self.instance.data_volume_size,
            })
            if quota_errors:
                raise serializers.ValidationError(
                    "One or more quotas are over limit: \n" + "\n".join(quota_errors))
        return value

    def validate(self, attrs):
        flavor = attrs.get('flavor')
        disk_size = attrs.get('disk_size')

        if flavor is not None and disk_size is not None:
            raise serializers.ValidationError("Cannot resize both disk size and flavor simultaneously")
        if flavor is None and disk_size is None:
            raise serializers.ValidationError("Either disk_size or flavor is required")
        return attrs


class TenantSerializer(structure_serializers.BaseResourceSerializer):

    service = serializers.HyperlinkedRelatedField(
        source='service_project_link.service',
        view_name='openstack-detail',
        read_only=True,
        lookup_field='uuid')

    service_project_link = serializers.HyperlinkedRelatedField(
        view_name='openstack-spl-detail',
        queryset=models.OpenStackServiceProjectLink.objects.all(),
        write_only=True)

    class Meta(structure_serializers.BaseResourceSerializer.Meta):
        model = models.Tenant
        view_name = 'openstack-tenant-detail'
        fields = structure_serializers.BaseResourceSerializer.Meta.fields + (
            'availability_zone', 'internal_network_id', 'external_network_id', 'user_username', 'user_password',
        )
        read_only_fields = structure_serializers.BaseResourceSerializer.Meta.read_only_fields + (
            'internal_network_id', 'external_network_id', 'user_password',
        )
        protected_fields = structure_serializers.BaseResourceSerializer.Meta.protected_fields + (
            'user_username',
        )

    def get_access_url(self, tenant):
        parsed = urlparse.urlparse(tenant.service_project_link.service.settings.backend_url)
        return '%s://%s/dashboard' % (parsed.scheme, parsed.hostname)

    def create(self, validated_data):
        spl = validated_data['service_project_link']
        # get availability zone from service settings if it is not defined
        if not validated_data.get('availability_zone'):
            validated_data['availability_zone'] = spl.service.settings.options.get('availability_zone', '')
        # init tenant user username(if not defined) and password
        if not validated_data.get('user_username'):
            name = validated_data['name']
            validated_data['user_username'] = slugify(name)[:30] + '-user'
        validated_data['user_password'] = core_utils.pwgen()
        return super(TenantSerializer, self).create(validated_data)


class LicenseSerializer(serializers.ModelSerializer):

    instance = serializers.SerializerMethodField()
    group = serializers.SerializerMethodField()
    type = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()

    class Meta:
        model = Tag
        fields = ('instance', 'group', 'type', 'name')

    def get_instance(self, obj):
        instance_ct = ContentType.objects.get_for_model(models.Instance)
        instance = obj.taggit_taggeditem_items.filter(tag=obj, content_type=instance_ct).first().content_object
        url_name = instance.get_url_name() + '-detail'
        return reverse.reverse(
            url_name, request=self.context['request'], kwargs={'uuid': instance.uuid.hex})

    def get_group(self, obj):
        try:
            return obj.name.split(':')[0]
        except IndexError:
            return ''

    def get_type(self, obj):
        try:
            return obj.name.split(':')[1]
        except IndexError:
            return ''

    def get_name(self, obj):
        try:
            return obj.name.split(':')[2]
        except IndexError:
            return ''
