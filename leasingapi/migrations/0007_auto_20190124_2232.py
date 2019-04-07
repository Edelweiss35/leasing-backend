# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2019-01-24 22:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leasingapi', '0006_legalposition_setting'),
    ]

    operations = [
        migrations.CreateModel(
            name='KeyText',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=255)),
            ],
        ),
        migrations.RemoveField(
            model_name='legalposition',
            name='text',
        ),
        migrations.AddField(
            model_name='legalposition',
            name='text',
            field=models.ManyToManyField(related_name='legal_positions', to='leasingapi.KeyText'),
        ),
    ]
