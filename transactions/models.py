from __future__ import unicode_literals

import binascii
import os

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

from users import models as user_models
from companies import models as company_models


class DocumentType(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=500)
    country = models.CharField(max_length=100)
    verification_field = models.CharField(max_length=100)  # use case TBD

    # TODO: include user fields/ pixels to match (future: automation)

    def __str__(self):
        return self.name

    def __repr__(self):
        return "<{} '{}': '{}'>".format(
            self.__class__.__name__,
            self.name, self.description)


# Handles the creation of all transactions
class TransactionManager(models.Manager):

    def create(self, email, company_id, version, document_type=None):
        # identify user, company
        # TODO: user get_or_create?
        user = user_models.User.objects.get(email=email)
        # TODO: get company. TEmp. need to extract company from the session token
        company = company_models.Company.objects.get(id=company_id)

        # create new token
        new_token = TransactionToken.objects.create()

        # create new transaction
        transaction = Transaction(user=user, transaction_token=new_token, company=company, version=version)
        transaction.save()
        return transaction


class Transaction(models.Model):

    # request info
    ui_type = models.CharField(max_length=30, default="single")

    # returned info
    js_result = models.CharField(max_length=30, blank=True)  # TODO temp; to update

    # metadata
    date_created = models.DateTimeField(default=timezone.now)
    date_completed = models.DateTimeField(default=timezone.now)
    version = models.CharField(max_length=10, )
    user_ip = models.CharField(max_length=15, blank=True)
    company_ip = models.CharField(max_length=15, blank=True)

    # references: many transactions to 1 user
    user = models.ForeignKey(user_models.User, on_delete=models.CASCADE)

    # references: many transactions to 1 company
    company = models.ForeignKey(company_models.Company, on_delete=models.CASCADE)

    # Relationship: 1 transaction to 1 API Key
    transaction_token = models.OneToOneField('TransactionToken', related_name='transaction',
                                             on_delete=models.CASCADE, verbose_name=_("TransactionToken")
                                             )

    # TODO: two competing way to customize transaction: doc_types or service. To decide
    # references: many transactions to 1 service
    # service = models.ForeignKey(service_models.Service, on_delete=models.CASCADE)

    # Relationship: Many document types to many transactions
    # This enables the merchant to request for various document types to be collected
    # document_type = models.ForeignKey(DocumentType, on_delete=models.CASCADE)  # Temp
    document_type = models.ManyToManyField(DocumentType)  # TODO: should this be a separate class?

    objects = TransactionManager()

    def __str__(self):
        return str(self.id)

    def __repr__(self):
        return "<{}: company_ip='{}', owner_id='{}', datetime_created='{}'>".format(
            self.__class__.__name__,
            self.company_ip, self.user, self.date_created)


# http://stackoverflow.com/questions/27043349/how-to-use-custom-token-model-in-django-rest-framework
# Adapted from rest_framework.authtoken.models.Token
@python_2_unicode_compatible
class TransactionToken(models.Model):
    """
    The default authorization token model.
    """
    key = models.CharField(_("Key"), max_length=40, primary_key=True)

    # don't need to link to a user
    # user = models.OneToOneField(
    #     settings.AUTH_USER_MODEL, related_name='transaction_token',
    #     on_delete=models.CASCADE, verbose_name=_("User")
    # )
    created = models.DateTimeField(_("Created"), auto_now_add=True)

    # relationship: 1 token have 1 transaction. referenced in the transaction table.
    # transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)

    class Meta:
        # Work around for a bug in Django:
        # https://code.djangoproject.com/ticket/19422
        #
        # Also see corresponding ticket:
        # https://github.com/tomchristie/django-rest-framework/issues/705
        abstract = 'rest_framework.authtoken' not in settings.INSTALLED_APPS
        verbose_name = _("TransactionToken")
        verbose_name_plural = _("TransactionTokens")

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        return super(TransactionToken, self).save(*args, **kwargs)

    def generate_key(self):
        return binascii.hexlify(os.urandom(20)).decode()

    def __str__(self):
        return self.key

    def __repr__(self):
        return "<{}: key = '{}'>".format(
            self.__class__.__name__, self.key)