# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-09-23 05:30
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20160922_0759'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='privilege',
            field=models.ForeignKey(blank=True, default=3, null=True, on_delete=django.db.models.deletion.CASCADE, to='users.Privilege'),
        ),
    ]
