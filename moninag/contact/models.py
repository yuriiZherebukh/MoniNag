from django.db import models

from registration.models import CustomUser


class Contact(models.Model):

    first_name = models.CharField(max_length=200, blank=None)
    second_name = models.CharField(max_length=200, blank=None)
    email = models.EmailField(blank=False, unique=True)
    is_active = models.BooleanField(default=False)
    activation_key = models.CharField(default='', max_length=1000, editable=False)
    user = models.ForeignKey(CustomUser)

    @staticmethod
    def create(first_name, second_name, email, user):

        contact = Contact()

        contact.first_name = first_name
        contact.second_name = second_name
        contact.email = email
        contact.user = user

        contact.save()

        return contact

    def update(self, first_name=None, second_name=None, email=None):

        if first_name:
            self.first_name = first_name
        if second_name:
            self.second_name = second_name
        if email:
            self.email = email

        self.save()

    @staticmethod
    def get_by_id(contact_id):
        """
        :param user_id: int - user id
        :return: QuerySet<Contact>: QuerySet of contact.
        """
        try:
            Contact.objects.get(id=contact_id)
            return Contact.objects.get(id=contact_id)
        except:
            return None

    @staticmethod
    def get_by_user_id(user_id):
        """
        :param user_id: int - user id
        :return: QuerySet<Contact>: QuerySet of contacts.
        """
        return Contact.objects.filter(user=user_id)

    def to_dict(self):
        """Convert model object to dictionary.

        :return: dict:
                {
                    'id': contact id,
                    'first_name': first name,
                    'second_name': second name,
                    'email': email
                }
        """

        return {
            'id': self.id,
            'first_name': self.first_name,
            'second_name': self.second_name,
            'email': self.email
        }