# Generated by Django 3.0.2 on 2020-01-31 07:04

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0002_auto_20200128_2352'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shipment',
            name='id',
            field=models.UUIDField(default=uuid.UUID('1bd23896-df85-4c28-8eb9-0df11a2f03f2'), primary_key=True, serialize=False),
        ),
    ]
