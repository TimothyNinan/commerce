# Generated by Django 3.0.8 on 2020-07-16 18:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0006_auto_20200716_1830'),
    ]

    operations = [
        migrations.AddField(
            model_name='listings',
            name='open',
            field=models.BooleanField(default=True),
        ),
    ]
