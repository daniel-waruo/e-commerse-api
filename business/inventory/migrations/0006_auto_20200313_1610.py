# Generated by Django 3.0.3 on 2020-03-13 13:10

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0005_auto_20200304_1732'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shipment',
            name='id',
            field=models.UUIDField(default=uuid.UUID('9d9049fc-3cca-44e3-8912-c717a0dcdf03'), primary_key=True, serialize=False),
        ),
    ]
