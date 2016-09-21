from __future__ import unicode_literals

import datetime
import binascii
import os

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

from companies import models as company_models

# from rest_framework.authtoken.models import Token


# # Temp; to remove
# class Document(models.Model):
#     document_text = models.CharField(max_length=200)
#     pub_date = models.DateTimeField('date published')


class Privilege(models.Model):
    name = models.CharField(max_length=30)

    # Admin
    all_write = models.BooleanField(default=False, )
    all_delete = models.BooleanField(default=False, )
    all_read = models.BooleanField(default=False, )
    all_verify = models.BooleanField(default=False, )

    # Business:
    company_read_transactions = models.BooleanField(default=False, )
    company_write_transactions = models.BooleanField(default=False, )
    company_verify_transactions = models.BooleanField(default=False, )
    company_delete_transactions = models.BooleanField(default=False, )

    company_read_documents = models.BooleanField(default=False, )
    company_write_documents = models.BooleanField(default=False, )
    company_verify_documents = models.BooleanField(default=False, )
    company_delete_documents = models.BooleanField(default=False, )

    # User's data:
    user_read = models.BooleanField(default=False, )
    user_write = models.BooleanField(default=False, )
    user_verify = models.BooleanField(default=False, )
    user_delete = models.BooleanField(default=False, )

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

    # relationship: many users have 1 privilege (This is the MAX privilege that they can use when creating session tokens)
    privilege = models.ForeignKey(Privilege, on_delete=models.CASCADE, blank=True, null=True, )

    # relationship: many users have 1 company (works for)
    company = models.ForeignKey(company_models.Company, on_delete=models.CASCADE, blank=True, null=True, )

    def __str__(self):
        return self.username

    def __repr__(self):
        return "<{} '{}': privilege='{}', registered='{}'>".format(
            self.__class__.__name__,
            self.email, self.privilege, self.is_registered)

    # example
    def was_registered_recently(self):
        return self.date_registered >= timezone.now() - datetime.timedelta(days=1)

    # def get_absolute_url(self):
    #     return reverse('users:detail', kwargs={'username': self.username})


# overrides AbstractUser defaults
User._meta.get_field('email').blank = False
# User._meta.get_field('email')._unique = True


# http://stackoverflow.com/questions/27043349/how-to-use-custom-token-model-in-django-rest-framework
# Adapted from rest_framework.authtoken.models.Token
# need full override since User now has one to many relationship with Tokens
@python_2_unicode_compatible
class SessionToken(models.Model):
    """
    The default authorization token model.
    """
    key = models.CharField(_("Key"), max_length=40, primary_key=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='session_token',
        on_delete=models.CASCADE, verbose_name=_("User")
    )
    created = models.DateTimeField(_("Created"), auto_now_add=True)

    # relationship: many tokens have 1 privilege. Note: all tokens must have a privilege
    privilege = models.ForeignKey(Privilege, on_delete=models.CASCADE)

    class Meta:
        # Work around for a bug in Django:
        # https://code.djangoproject.com/ticket/19422
        #
        # Also see corresponding ticket:
        # https://github.com/tomchristie/django-rest-framework/issues/705
        abstract = 'rest_framework.authtoken' not in settings.INSTALLED_APPS
        verbose_name = _("SessionToken")
        verbose_name_plural = _("SessionTokens")

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        return super(SessionToken, self).save(*args, **kwargs)

    def generate_key(self):
        return binascii.hexlify(os.urandom(20)).decode()

    def __str__(self):
        return self.key

    def __repr__(self):
        return "<{} '{}': transaction='{}'>".format(
            self.__class__.__name__,
            self.key, self.transaction)
