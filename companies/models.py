from __future__ import unicode_literals

import datetime

from django.contrib.auth.models import AbstractUser
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

# from transactions import models as transaction_models

# class ApiKey(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     api_key = db.Column(db.Integer)
#
#     # access_rights
#     read_data = db.Column(db.Boolean)
#     update_data = db.Column(db.Boolean)
#     create_transaction = db.Column(db.Boolean)
#
#     # metadata
#     datetime_start = db.Column(db.DateTime, default=datetime.datetime.utcnow)
#     datetime_end = db.Column(db.DateTime)
#
#     # references: (1 or many) api_keys to 1 company
#     company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
#
#     def __repr__(self):
#         return "<{}: company_id='{}', api_key='{}', datetime_start='{}', datetime_end='{}'>".format(
#             self.__class__.__name__,
#             self.company_id, self.api_key, self.datetime_start, self.datetime_end)
#
#     @property
#     def serialize(self):
#         return {
#             'id': self.id,
#             'api_key': self.api_key,
#             'datetime_start': self.datetime_start,
#             'datetime_end': self.datetime_end
#
#         }


class Company(models.Model):
    name = models.CharField(max_length=100)
    white_label = models.BooleanField(default=False,)

    is_active = models.BooleanField(default=False, )
    date_registered = models.DateTimeField(_('date registered'), default=timezone.now)

    # references: 1 to many # TODO
    # forms = relationship("Form", backref="company")

    # references: 1 to many
    # transactions (done)
    # addresses (done)

    def __str__(self):
        return self.name

    def __repr__(self):
        return "<{} '{}': name='{}'>".format(
            self.__class__.__name__,
            self.id, self.name)
