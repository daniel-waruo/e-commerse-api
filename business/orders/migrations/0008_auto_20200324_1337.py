# Generated by Django 3.0.4 on 2020-03-24 10:37

from django.db import migrations
import shortuuidfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0007_auto_20200318_1351'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='id',
            field=shortuuidfield.fields.ShortUUIDField(blank=True, default='U5KFpneeA5qEDEfi2yWLhB', editable=False, max_length=22, primary_key=True, serialize=False),
        ),
    ]
