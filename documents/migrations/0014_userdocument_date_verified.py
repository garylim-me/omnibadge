# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-09-23 00:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0013_userdocument_version'),
    ]

    operations = [
        migrations.AddField(
            model_name='userdocument',
            name='date_verified',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
