# Generated by Django 3.0.3 on 2020-03-03 19:09

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0003_auto_20200303_2200'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shipment',
            name='id',
            field=models.UUIDField(default=uuid.UUID('0323240a-6eb6-4a79-a2b2-aa2ed2c271c7'), primary_key=True, serialize=False),
        ),
    ]
