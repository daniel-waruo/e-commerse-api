# Generated by Django 3.0.7 on 2020-06-15 13:42

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0012_auto_20200605_1447'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shipment',
            name='id',
            field=models.UUIDField(default=uuid.UUID('7ef2a27a-4868-48e5-ae4e-cfc7180dcf76'), primary_key=True, serialize=False),
        ),
    ]