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


class Service(models.Model):
    name = models.CharField(max_length=30)

    # basic features
    verify_passport = models.BooleanField(default=False,)
    verify_govt_id = models.BooleanField(default=False,)

    # standard verification features
    live_image = models.BooleanField(default=False,)
    verify_nric_ica = models.BooleanField(default=False,)
    verify_billing_address = models.BooleanField(default=False,)
    verify_mobile_number = models.BooleanField(default=False,)

    # user management features (to move to new section, pegged to company-users next time?)
    track_expiry = models.BooleanField(default=False, )
    follow_up_request = models.BooleanField(default=False, )
    network_sharing = models.BooleanField(default=False, )

    # premium verification features
    fast_verification = models.BooleanField(default=False, )
    phone_interviews = models.BooleanField(default=False, )

    # references: 1 service to many transactions TODO
    # transactions = relationship("Transaction", backref="service")

    def __str__(self):
        return self.name

    def __repr__(self):
        return "<{} '{}': name='{}'>".format(
            self.__class__.__name__,
            self.id, self.name)


class ServiceSubscription(models.Model):
    name = models.CharField(max_length=100)
    price_per_user = models.DecimalField(max_digits=10, decimal_places=4)

    date_start = models.DateTimeField(default=timezone.now)
    date_end = models.DateTimeField(blank=True, null=True, )

    # relationship: many service subscriptions have 1 company
    company = models.ForeignKey(company_models.Company, on_delete=models.CASCADE, blank=True, null=True, )  # null is temp?

    # relationship: many service subscriptions have 1 service
    service = models.ForeignKey(Service, on_delete=models.CASCADE, null=True, )  # null is temp

    def __str__(self):
        return self.name

    def __repr__(self):
        return "<{}: company_id='{}', service_id='{}', datetime_start='{}', datetime_end='{}'>".format(
            self.__class__.__name__,
            self.company, self.service, self.datetime_start, self.datetime_end)
