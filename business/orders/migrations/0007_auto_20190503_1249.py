# Generated by Django 2.1.5 on 2019-05-03 09:49

import uuid

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('ordersapp', '0006_auto_20190503_1249'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='id',
            field=models.UUIDField(default=uuid.UUID('8c8b662c-b8c5-4b12-affb-f4aaf523c870'), editable=False,
                                   primary_key=True, serialize=False),
        ),
    ]
