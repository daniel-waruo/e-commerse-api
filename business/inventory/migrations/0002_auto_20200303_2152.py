# Generated by Django 3.0.3 on 2020-03-03 18:52

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
            field=models.UUIDField(default=uuid.UUID('97137e88-8c7a-423a-adf5-b29b5c5a737b'), primary_key=True, serialize=False),
        ),
    ]
