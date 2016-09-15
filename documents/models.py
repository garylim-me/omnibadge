from __future__ import unicode_literals

import datetime

from django.contrib.auth.models import AbstractUser
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from users import models as user_models
from transactions import models as transaction_models


# Handles the creation of all document types
class DocumentManager(models.Manager):

    def create_doc(self, user, doc_type, **kwargs):
        if doc_type == "Form":
            doc_class = DocForm
            document_type = transaction_models.DocumentType.objects.get(name="Form")
        elif doc_type == "Passport":
            doc_class = DocPassport
            document_type = transaction_models.DocumentType.objects.get(name="Passport")
        else:
            raise ValueError("doc_type is not supported.")

        doc_object = doc_class.objects.create(user=user, document_type=document_type, **kwargs)
        user_doc = self.create(user=user, document_object=doc_object)
        return user_doc


# All documents have to be created via this model!
# Links Users to any type of document
class UserDocument(models.Model):

    # This is a duplicate field as in the abstract class since we don't actually want to query this table for user data
    # references: many documents to 1 user
    user = models.ForeignKey(user_models.User, on_delete=models.CASCADE)

    # https://docs.djangoproject.com/en/dev/ref/contrib/contenttypes/#generic-relations
    document_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)  # blanks are temp
    document_id = models.PositiveIntegerField()  # blanks are temp
    document_object = GenericForeignKey('document_type', 'document_id')

    objects = DocumentManager()

    def __str__(self):
        return str(self.id)

    def __repr__(self):
        return "<{}: id='{}', doc_type='{}', doc_id='{}', user='{}'>".format(
            self.__class__.__name__, self.id, self.document_type, self.document_id, self.user)


# This is an abstract model! Contains generic information needed for all documents.
class Document(models.Model):
    date_created = models.DateTimeField(default=timezone.now)
    version = models.CharField(max_length=10, )

    # verification
    verified = models.BooleanField(default=False,)
    date_verified = models.DateTimeField(blank=True, null=True, )

    # references: many documents to 1 transaction
    transaction = models.ForeignKey(transaction_models.Transaction, on_delete=models.CASCADE)

    # references: many documents to 1 user
    user = models.ForeignKey(user_models.User, on_delete=models.CASCADE)

    # references: many documents to 1 document type  # TODO: This don't make sense to be a selectable. KIV.
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


class DocForm(Document):

    # provided data
    first_name = models.CharField(max_length=100, blank=True, )
    last_name = models.CharField(max_length=100, blank=True, )
    nationality = models.CharField(max_length=100, blank=True, )
    dob = models.DateTimeField(blank=True, null=True, )
    mobile = models.CharField(max_length=100, blank=True, )
    home = models.CharField(max_length=100, blank=True, )
    other = models.CharField(max_length=100, blank=True, )
