# Generated by Django 2.2.6 on 2019-10-07 13:41

import uuid

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('inventory', '0006_auto_20191007_1353'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shipment',
            name='id',
            field=models.UUIDField(default=uuid.UUID('673d7774-4093-42e1-9dc6-9f746efc00a7'), primary_key=True,
                                   serialize=False),
        ),
    ]
