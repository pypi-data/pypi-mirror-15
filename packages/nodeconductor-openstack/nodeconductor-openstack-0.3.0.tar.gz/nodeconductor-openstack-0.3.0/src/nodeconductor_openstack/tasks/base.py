from celery import shared_task, current_app
from functools import wraps

from nodeconductor.core.tasks import retry_if_false, BackendMethodTask, Task
from nodeconductor.core.utils import deserialize_instance

from .. import models
from ..backend import OpenStackClient


def track_openstack_session(task_fn):
    @wraps(task_fn)
    def wrapped(tracked_session, *args, **kwargs):
        client = OpenStackClient(session=tracked_session)
        task_fn(client, *args, **kwargs)
        return client.session
    return wrapped


def save_error_message_from_task(func):
    @wraps(func)
    def wrapped(task_uuid, *args, **kwargs):
        func(*args, **kwargs)
        result = current_app.AsyncResult(task_uuid)
        transition_entity = kwargs['transition_entity']
        message = result.result['exc_message']
        if message:
            transition_entity.error_message = message
            transition_entity.save(update_fields=['error_message'])
    return wrapped


@shared_task
@track_openstack_session
def nova_server_resize(client, server_id, flavor_id):
    client.nova.servers.resize(server_id, flavor_id, 'MANUAL')


@shared_task
@track_openstack_session
def nova_server_resize_confirm(client, server_id):
    client.nova.servers.confirm_resize(server_id)


@shared_task(max_retries=300, default_retry_delay=3)
@track_openstack_session
@retry_if_false
def nova_wait_for_server_status(client, server_id, status):
    server = client.nova.servers.get(server_id)
    return server.status == status


@shared_task
def delete_tenant_with_spl(serialized_tenant):
    tenant = deserialize_instance(serialized_tenant)
    spl = tenant.service_project_link
    tenant.delete()
    spl.delete()


# TODO: move this signal to itacloud assembly application
@shared_task
def register_instance_in_zabbix(instance_uuid):
    from nodeconductor.template.zabbix import register_instance
    instance = models.Instance.objects.get(uuid=instance_uuid)
    register_instance(instance)


# Temporary task. Should be removed after tenant will be connected to instance.
class SecurityGroupCreationTask(BackendMethodTask):
    """ Create tenant for SPL if it does not exist and execute backend method """

    def create_tenant(self, spl, security_group):
        """ Create tenant for SPL via executor.

        Creation ignores security groups pull to avoid new group deletion.
        """
        from nodeconductor_openstack import executors

        tenant = spl.create_tenant()
        executors.TenantCreateExecutor.execute(tenant, async=False, pull_security_groups=False)
        tenant.refresh_from_db()
        if tenant.state != models.Tenant.States.OK:
            security_group.set_erred()
            security_group.error_message = 'Tenant %s (PK: %s) creation failed.' % (tenant, tenant.pk)
            security_group.save()
        return tenant

    def execute(self, security_group, *args, **kwargs):
        spl = security_group.service_project_link
        if spl.tenant is None:
            from nodeconductor_openstack import executors
            # Create tenant without security groups
            tenant = self.create_tenant(spl, security_group)
            # Create new security group
            backend = tenant.get_backend()
            backend.create_security_group(security_group)
            # Pull all security groups
            executors.TenantPullSecurityGroupsExecutor.execute(tenant, async=False)
        else:
            super(SecurityGroupCreationTask, self).execute(security_group, 'create_security_group', *args, **kwargs)


class RuntimeStateException(Exception):
    pass


class PollRuntimeStateTask(Task):
    max_retries = 300
    default_retry_delay = 5

    def get_backend(self, instance):
        return instance.get_backend()

    def execute(self, instance, backend_pull_method, success_state, erred_state):
        backend = self.get_backend(instance)
        getattr(backend, backend_pull_method)(instance)
        instance.refresh_from_db()
        if instance.runtime_state not in (success_state, erred_state):
            self.retry()
        elif instance.runtime_state == erred_state:
            raise RuntimeStateException(
                'Instance %s (PK: %s) runtime state become erred: %s' % (instance, instance.pk, erred_state))
