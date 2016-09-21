# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-09-21 01:00
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('transactions', '0002_transaction_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='TransactionToken',
            fields=[
                ('key', models.CharField(max_length=40, primary_key=True, serialize=False, verbose_name='Key')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('transaction', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='transactions.Transaction')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='transaction_token', to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'abstract': False,
                'verbose_name': 'TransactionToken',
                'verbose_name_plural': 'TransactionTokens',
            },
        ),
    ]