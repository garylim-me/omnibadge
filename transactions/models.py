from __future__ import unicode_literals

import datetime

from django.contrib.auth.models import AbstractUser
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

from users import models as user_models
from companies import models as company_models
from services import models as service_models


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


class Transaction(models.Model):

    # request info
    ui_type = models.CharField(max_length=30, default="single")

    # returned info
    transaction_token = models.CharField(max_length=30, )  # temp; to update
    js_result = models.CharField(max_length=30, )  # TODO temp; to update

    # metadata
    date_created = models.DateTimeField(default=timezone.now)
    date_completed = models.DateTimeField(default=timezone.now)
    version = models.CharField(max_length=10, )
    user_ip = models.CharField(max_length=15, )
    company_ip = models.CharField(max_length=15, )

    # references: many transactions to 1 user
    user = models.ForeignKey(user_models.User, on_delete=models.CASCADE)

    # references: many transactions to 1 service
    service = models.ForeignKey(service_models.Service, on_delete=models.CASCADE)

    # references: many transactions to 1 company
    company = models.ForeignKey(company_models.Company, on_delete=models.CASCADE)

    # references: many transactions to 1
    # company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    # form_id = db.Column(db.Integer, db.ForeignKey('form.id'))

    # Relationship: Many document types to many transactions
    # This enables the merchant to request for various document types to be collected
    # document_type = models.ForeignKey(DocumentType, on_delete=models.CASCADE)  # Temp
    document_type = models.ManyToManyField(DocumentType)  # TODO: should this be a separate class?

    # Relationship: Many transactions to 1 API Keys
    # connect the API keys? TBC

    def __str__(self):
        return str(self.id)

    def __repr__(self):
        return "<{}: company_ip='{}', owner_id='{}', datetime_created='{}'>".format(
            self.__class__.__name__,
            self.company_ip, self.owner_id, self.datetime_created)
