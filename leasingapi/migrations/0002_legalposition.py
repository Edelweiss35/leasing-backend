# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2019-01-07 22:07
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('leasingauth', '0002_leasingclientinvitetoken'),
        ('leasingapi', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='LegalPosition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('clause_name', models.CharField(max_length=255)),
                ('text', models.CharField(max_length=255)),
                ('reason', models.TextField()),
                ('action', models.CharField(choices=[('NFD', 'Not Found'), ('FND', 'Found')], default='NFD', max_length=3)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='legal_positions', to='leasingauth.LeasingClient')),
            ],
            options={
                'verbose_name_plural': 'Legal Positions',
            },
        ),
    ]
