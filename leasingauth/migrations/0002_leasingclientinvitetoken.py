# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2019-01-04 05:46
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('leasingauth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='LeasingClientInviteToken',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('invite_token', models.CharField(max_length=255, unique=True)),
                ('client', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='client_token', to='leasingauth.LeasingClient')),
            ],
        ),
    ]