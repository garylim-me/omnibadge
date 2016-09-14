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
from documents import models as document_models


class Address(models.Model):
    name = models.CharField(max_length=30, blank=True, )  # Optional field if the user wants to name the address
    address_type = models.CharField(max_length=30)  # Form, User, Company, DocPassport, DocNRIC

    address_line_1 = models.CharField(max_length=120)
    address_line_2 = models.CharField(max_length=120, blank=True, )
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=30)
    postal_code = models.CharField(max_length=15)

    # a user can have multiple addresses, some old and inactive
    is_active = models.BooleanField(default=False,)

    # relationship: many addresses have 1 or 0 user (can also belong to a form)
    user = models.ForeignKey(user_models.User, on_delete=models.CASCADE, null=True, blank=True, )

    # relationship: many addresses have 1 or 0 company (can also belong to a form)
    company = models.ForeignKey(company_models.Company, on_delete=models.CASCADE, null=True, blank=True, )

    # relationship: many addresses have 1 or 0 form (can also belong to a form)
    doc_form = models.ForeignKey(document_models.DocForm, on_delete=models.CASCADE, null=True, blank=True, )

    # references: 1 address to many forms
    # forms = relationship("Form", backref="address")

    # references: (1 or many) addresses to 1 user/company/country
    # user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    # company_id = db.Column(db.Integer, db.ForeignKey('company.id'))
    # country_id = db.Column(db.Integer, db.ForeignKey('country.id'), nullable=False)

    def __str__(self):
        return "Address Type: " + self.address_type

    def __repr__(self):
        return "<{}: address_type='{}', address_line_1='{}'>".format(
            self.__class__.__name__,
            self.address_type, self.address_line_1)


# Not used yet
class Country(models.Model):
    name = models.CharField(max_length=60)

    def __str__(self):
        return self.name

    def __repr__(self):
        return "<{}: name='{}'>".format(self.__class__.__name__, self.name)
