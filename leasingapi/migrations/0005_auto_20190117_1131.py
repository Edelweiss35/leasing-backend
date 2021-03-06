# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2019-01-17 11:31
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('leasingapi', '0004_auto_20190110_0500'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExportResult',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ammend_number', models.TextField(blank=True, null=True)),
                ('clause_number', models.TextField()),
                ('clause_name', models.TextField()),
                ('Lease_required_amendment', models.TextField(blank=True, null=True)),
                ('lessor_response', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='legalposition',
            name='export_result',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='export_result', to='leasingapi.ExportResult'),
        ),
    ]
