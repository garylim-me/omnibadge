# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-09-23 04:36
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0014_userdocument_date_verified'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userdocument',
            name='transactions',
        ),
    ]
