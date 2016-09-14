from __future__ import unicode_literals

import datetime

from django.contrib.auth.models import AbstractUser
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

from users import models as user_models
from transactions import models as transaction_models


# TODO: ADD FORM

class Document(models.Model):
    date_created = models.DateTimeField(default=timezone.now)
    version = models.CharField(max_length=10, )

    # verification
    verified = models.BooleanField(default=False,)
    date_verified = models.DateTimeField(blank=True, )

    # references: many documents to 1 transaction
    transaction = models.ForeignKey(transaction_models.Transaction, on_delete=models.CASCADE)

    # references: many documents to 1 user
    user = models.ForeignKey(user_models.User, on_delete=models.CASCADE)

    # references: many documents to 1 document type
    document_type = models.ForeignKey(transaction_models.DocumentType, on_delete=models.CASCADE)

    class Meta:
        abstract = True

    def __str__(self):
        return str(self.id)

    def __repr__(self):
        return "<{}: company_ip='{}', owner_id='{}', datetime_created='{}'>".format(
            self.__class__.__name__,
            self.document_type, self.user, self.transaction)


class DocPassport(Document):

    # user input/verify data
    document_image = models.CharField(max_length=30, )
    document_filename = models.CharField(max_length=100, )  # location of stored file in S3
    document_filename2 = models.CharField(max_length=100, )  # location of stored file in S3

    # parsed data
    parsed_passport_id = models.CharField(max_length=100, blank=True, )
    parsed_first_name = models.CharField(max_length=100, blank=True, )
    parsed_last_name = models.CharField(max_length=100, blank=True, )
    parsed_nationality = models.CharField(max_length=100, blank=True, )
    parsed_dob = models.DateTimeField(blank=True, null=True)
    parsed_issue_date = models.DateTimeField(blank=True, null=True)
    parsed_expiry_date = models.DateTimeField(blank=True, null=True)

    # TODO: reference session_id and user data snapshot


class DocForm(Document):

    # provided data
    first_name = models.CharField(max_length=100, blank=True, )
    last_name = models.CharField(max_length=100, blank=True, )
    nationality = models.CharField(max_length=100, blank=True, )
    dob = models.DateTimeField(blank=True, null=True, )
    mobile = models.CharField(max_length=100, blank=True, )
    home = models.CharField(max_length=100, blank=True, )
    other = models.CharField(max_length=100, blank=True, )