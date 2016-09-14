# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-09-14 09:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0002_docform'),
    ]

    operations = [
        migrations.AlterField(
            model_name='docform',
            name='dob',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='docpassport',
            name='parsed_dob',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='docpassport',
            name='parsed_expiry_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='docpassport',
            name='parsed_issue_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
