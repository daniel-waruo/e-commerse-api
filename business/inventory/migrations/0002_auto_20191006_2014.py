# Generated by Django 2.2.6 on 2019-10-06 17:14

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shipment',
            name='id',
            field=models.UUIDField(default=uuid.UUID('026d16f2-d3e6-477b-8988-547f3bd60b44'), primary_key=True, serialize=False),
        ),
    ]
