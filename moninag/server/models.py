"""This module holds Server model class"""
from django.db import models

from registration.models import CustomUser

STATE_CHOICES = (
    ('', "NotSelected"),
    ('prod', "Production"),
    ('stag', "Staging"),
)


class Server(models.Model):
    """
    Server

    :argument id: int - autogenerated primary key
    :argument name: str - Server name
    :argument address: str - Server address
    :argument state: str - Server state ('NotSelected'/'Production','Staging')
    :argument user: id - CustomUser id - user owner id
    """

    name = models.CharField(max_length=50)
    address = models.CharField(max_length=200)
    state = models.CharField(max_length=20, choices=STATE_CHOICES, default='')
    user = models.ForeignKey(CustomUser, default=1, on_delete=models.CASCADE)

    @staticmethod
    def create(name, address, state, user_id):
        """Create and add server to database.

        :param name: str - server name
        :param address: str - server address
        :param state: str - server state
        :param user: user
        :return: Created server for success, None otherwise.
        """

        server = Server()
        server.name = name
        server.address = address
        server.state = state
        server.user = CustomUser.objects.get(id=user_id)
        server.save()
        return server

    def update(self, name=None, address=None, state=None):
        """Update server data.

        :param name: server name
        :param address: server address
        :param state: server state
        :return: The return value. Updated server for success, None otherwise.
        """

        # Check if server exist allready
        if name:
            self.name = name
        if address:
            self.address = address
        if state:
            self.state = state
        self.save()

        return self

    @staticmethod
    def get_by_id(id):
        """Get server with given id.

        :param id: server id
        :return: Server if server was found, and None otherwise.
        """
        try:
            server = Server.objects.get(id=id)
        except Exception as error:
            return None

        return server

    @staticmethod
    def get_by_user_id(user_id):
        """
        :param user_id:
        :return: return Server
        """
        return Server.objects.filter(user=user_id)

    @staticmethod
    def get(states=None, user_id=None, start=0, end=20):
        """Get servers.

        :param states: server state - optional parameter - used as filter
        :param user_id: user id - optional parameter - used as filter
        :param start: starting index of servers returned
        :param end: las index of servers returned.
        :return: QuerySet<Server>: QuerySet of servers.
        """

        filters = {}

        if states:
            filters['state__in'] = states
        if user_id:
            filters['user__id'] = user_id
        if filters:
            servers = Server.objects.filter(**filters)
        else:
            servers = Server.objects.all()[start:end]

        return servers

    def to_dict(self):
        """Convert model object to dictionary.

        :return: dict:
                {
                    'id': id,
                    'name': name,
                    'address': address.
                    'state': state,
                    'user_id': user.id
                }
        """

        return {
            'id': self.id,
            'name': self.name,
            'address': self.address,
            'state': self.state,
            'user_id': self.user.id
        }

    def __str__(self):
        return "ServerId: {}, ServerName: {}, ServerAddress: {}, ServerState {}".format(self.id,
                                                                                        self.name,
                                                                                        self.address,
                                                                                        self.state)
