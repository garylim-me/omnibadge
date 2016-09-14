from __future__ import unicode_literals

import datetime

from django.contrib.auth.models import AbstractUser
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone


# # Temp; to remove
# class Document(models.Model):
#     document_text = models.CharField(max_length=200)
#     pub_date = models.DateTimeField('date published')


class Privilege(models.Model):
    name = models.CharField(max_length=30)
    access_all_read = models.BooleanField(default=False,)
    access_all_write = models.BooleanField(default=False,)
    access_all_verify = models.BooleanField(default=False,)
    access_company_read = models.BooleanField(default=False,)
    access_company_write = models.BooleanField(default=False,)
    access_company_verify = models.BooleanField(default=False,)

    def __str__(self):
        return self.name

    def __repr__(self):
        return "<{} '{}': name='{}'>".format(
            self.__class__.__name__,
            self.id, self.name)


@python_2_unicode_compatible
class User(AbstractUser):
    # Email, username, first_name, last_name, password, last_login, date_joined, is_active, is_staff
    # already handled by Abstract user

    # note: registering (by user) is different from joining (auto-created by system)
    is_registered = models.BooleanField(default=False,)
    date_registered = models.DateTimeField(_('date registered'), default=timezone.now)

    # optional field; for future use. Not storing these information for now
    phone = models.CharField(max_length=30, blank=True, )

    # relationship: many users have 1 privilege
    privilege = models.ForeignKey(Privilege, on_delete=models.CASCADE, blank=True, null=True, )

    def __str__(self):
        return self.username

    def __repr__(self):
        return "<{} '{}': privilege='{}', registered='{}'>".format(
            self.__class__.__name__,
            self.email, self.privilege.name, self.is_registered)

    # example
    def was_registered_recently(self):
        return self.date_registered >= timezone.now() - datetime.timedelta(days=1)

    # def get_absolute_url(self):
    #     return reverse('users:detail', kwargs={'username': self.username})


# overrides AbstractUser defaults
User._meta.get_field('email').blank = False
# User._meta.get_field('email')._unique = True
