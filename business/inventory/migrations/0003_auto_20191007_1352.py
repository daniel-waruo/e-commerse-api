# Generated by Django 2.2.6 on 2019-10-07 10:52

import uuid

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('inventory', '0002_auto_20191006_2014'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shipment',
            name='id',
            field=models.UUIDField(default=uuid.UUID('1e1a3e02-2466-45c3-a6de-f3b8ada9083f'), primary_key=True,
                                   serialize=False),
        ),
    ]
