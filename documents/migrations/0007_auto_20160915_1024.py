# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-09-15 10:24
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0006_auto_20160915_0905'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdocument',
            name='document_id',
            field=models.PositiveIntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='userdocument',
            name='document_type',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType'),
            preserve_default=False,
        ),
    ]
