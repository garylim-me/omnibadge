# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-09-21 02:23
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0003_transactiontoken'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transactiontoken',
            name='transaction',
        ),
        migrations.RemoveField(
            model_name='transactiontoken',
            name='user',
        ),
        migrations.AlterField(
            model_name='transaction',
            name='company_ip',
            field=models.CharField(blank=True, max_length=15),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='js_result',
            field=models.CharField(blank=True, max_length=30),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='transaction_token',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='transaction', to='transactions.TransactionToken', verbose_name='TransactionToken'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='user_ip',
            field=models.CharField(blank=True, max_length=15),
        ),
    ]