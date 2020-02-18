# Generated by Django 3.0.2 on 2020-02-07 08:26

from django.db import migrations
import shortuuidfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_auto_20200131_1004'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='id',
            field=shortuuidfield.fields.ShortUUIDField(blank=True, default='RjygiDXHRvKyxo4M5U4yHk', editable=False, max_length=22, primary_key=True, serialize=False),
        ),
    ]