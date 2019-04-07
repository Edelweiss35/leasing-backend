# Generated by Django 2.1.5 on 2019-02-11 11:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('leasingauth', '0002_leasingclientinvitetoken'),
    ]

    operations = [
        migrations.AlterField(
            model_name='leasingclientinvitetoken',
            name='client',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='client_token', to='leasingauth.LeasingClient'),
        ),
    ]