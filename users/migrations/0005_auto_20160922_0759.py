# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-09-22 07:59
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_user_company'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sessiontoken',
            name='privilege',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='users.Privilege'),
            preserve_default=False,
        ),
    ]
