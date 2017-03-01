"""This module holds Check model class and basic functions"""
from django.db import models

from nagplugin.models import NagPlugin
from service.models import Service


class Check(models.Model):
    """Check model class

    :attribute id: int - Autogenerated primary key.
    :attribute name: str - Check name
    :attribute plugin: NagPlugin - ForeignKey to nagios plugin.
    :attribute status: status of current check
    :attribute last_run: time of last check run
    :attribute output: full check command output
    :attribute target_port: int - Define target port.
    :attribute run_freq: int - Define run frequency of plugin.
    :attribute service: int - ForeignKey to service id value.
    :attribute state: state of current check.
    """

    name = models.CharField(max_length=20, default=0)
    plugin = models.ForeignKey(NagPlugin, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, null=True, blank=True)
    last_run = models.DateTimeField(null=True, blank=True)
    output = models.CharField(max_length=200, null=True, blank=True)
    target_port = models.IntegerField(default=0)
    run_freq = models.IntegerField(default=0)
    service = models.ForeignKey(Service)
    state = models.BooleanField(default=True)

    @staticmethod
    def create(name, plugin, target_port, run_freq, service):
        """Create and add check to database.

        :param name: str - Check name.
        :param plugin: NagPlugin - Nagios plugin.
        :param target_port: int - Target port.
        :param run_freq: int - Run frequency.
        :param service: int - Service id.

        :return: Created check for success.
        """

        check = Check()

        check.name = name
        check.plugin = plugin
        check.target_port = target_port
        check.run_freq = run_freq
        check.service = service

        check.save()

        return check

    def update(self, name=None, plugin=None, target_port=None, run_freq=None, state=None):
        """Update check data.

        :param name: str - Check name.
        :param plugin: NagPlugin - Nagios plugin.
        :param target_port: int - Target port.
        :param run_freq: int - Run frequency.
        :param state: boolean - Run frequency.
        """
        if name:
            self.name = name
        if plugin:
            self.plugin = plugin
        if target_port:
            self.target_port = target_port
        if run_freq:
            self.run_freq = run_freq
        if state == False:
            self.state = state

        self.save()

    def update_service_status(self):
        """
        This method updates service status depending on this services checks statuses
        """

        checks = Check.objects.filter(service=self.service.id)
        statuses = [check.status for check in checks]

        if 'FAIL' in statuses:
            self.service.status = 'FAIL'
        elif 'WARNING' in statuses:
            self.service.status = 'WARNING'
        elif all(status == 'OK' for status in statuses):
            self.service.status = 'OK'

        self.service.save()

    @staticmethod
    def get_by_id(id):
        """Get check with given id.

        :param id: int - Check id.

        :return: Check object if check was found, and None otherwise.
        """

        try:
            check = Check.objects.get(id=id)
        except:
            return None

        return check

    @staticmethod
    def get_by_user_id(user_id):
        """Get checks by user id.

        :param user_id: int - User id.
        :return: QuerySet of checks for given user id.
        """

        checks = Check.objects.filter(service__server__user__id=user_id)

        return checks
    
    @staticmethod
    def get_by_service(service):
        """Get checks by user id.

        :param user_id: int - User id.
        :return: QuerySet of checks for given user id.
        """

        checks = Check.objects.filter(service=service)

        return checks

    def to_dict(self):
        """Convert model object to dictionary.

        :return: dict:
                {
                    'id': check id,
                    'name': check name,
                    'plugin_id': nagios plugin id,
                    'target_port': target port,
                    'run_freq': run frequency,
                    'service_id': service id
                }
        """

        return {
            'id': self.id,
            'name': self.name,
            'plugin_id': self.plugin.id,
            'status': self.status,
            'last_run': self.last_run,
            'output': self.output,
            'target_port': self.target_port,
            'run_freq': self.run_freq,
            'service_id': self.service.id,
            'state': self.state,
        }
