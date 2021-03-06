# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-09-23 04:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0015_remove_userdocument_transactions'),
        ('transactions', '0004_auto_20160921_0223'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='user_documents',
            field=models.ManyToManyField(blank=True, related_name='transactions', to='documents.UserDocument'),
        ),
    ]
