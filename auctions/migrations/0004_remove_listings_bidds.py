# Generated by Django 3.0.8 on 2020-07-15 17:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_auto_20200715_1536'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='listings',
            name='bidds',
        ),
    ]
