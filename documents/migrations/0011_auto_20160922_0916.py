# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-09-22 09:16
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0010_auto_20160922_0800'),
    ]

    operations = [
        migrations.RenameField(
            model_name='docform',
            old_name='transaction',
            new_name='transactions',
        ),
        migrations.RenameField(
            model_name='docpassport',
            old_name='transaction',
            new_name='transactions',
        ),
    ]
