# Generated by Django 3.0.8 on 2020-07-16 18:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_auto_20200715_1746'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bids',
            name='won',
        ),
        migrations.RemoveField(
            model_name='listings',
            name='open',
        ),
        migrations.AddField(
            model_name='listings',
            name='winner',
            field=models.ForeignKey(blank=True, default=1, on_delete=django.db.models.deletion.CASCADE, related_name='bidder', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='listings',
            name='lister',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='poster', to=settings.AUTH_USER_MODEL),
        ),
    ]