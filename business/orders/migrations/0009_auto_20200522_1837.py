# Generated by Django 3.0.4 on 2020-05-22 15:37

from django.db import migrations
import shortuuidfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0008_auto_20200324_1337'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='id',
            field=shortuuidfield.fields.ShortUUIDField(blank=True, default='UGk5JJBPLZCJRzj4LS52Zj', editable=False, max_length=22, primary_key=True, serialize=False),
        ),
    ]
