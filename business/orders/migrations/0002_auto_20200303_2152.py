# Generated by Django 3.0.3 on 2020-03-03 18:52

from django.db import migrations
import shortuuidfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='id',
            field=shortuuidfield.fields.ShortUUIDField(blank=True, default='GkNY6An2zot5DewkaPrLqH', editable=False, max_length=22, primary_key=True, serialize=False),
        ),
    ]