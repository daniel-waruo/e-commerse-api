# Generated by Django 3.0.3 on 2020-03-04 14:32

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0004_auto_20200303_2209'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shipment',
            name='id',
            field=models.UUIDField(default=uuid.UUID('67ae44e4-8f5a-450f-912f-32525a9d4e10'), primary_key=True, serialize=False),
        ),
    ]