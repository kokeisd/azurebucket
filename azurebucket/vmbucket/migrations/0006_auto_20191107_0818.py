# Generated by Django 2.2.6 on 2019-11-07 08:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vmbucket', '0005_auto_20191107_0817'),
    ]

    operations = [
        migrations.RenameField(
            model_name='vmbucket',
            old_name='primary_ip',
            new_name='primary_ip_address',
        ),
        migrations.RenameField(
            model_name='vmbucket',
            old_name='secondary_ips',
            new_name='secondary_ip_addresses',
        ),
    ]
