# Generated by Django 3.0.8 on 2020-07-07 15:25

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('personal', '0005_auto_20200707_1516'),
    ]

    operations = [
        migrations.AddField(
            model_name='personal',
            name='birthday',
            field=models.DateField(blank=True, default=datetime.datetime(2020, 7, 7, 15, 25, 40, 887886, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
