# Generated by Django 3.0.4 on 2020-03-18 10:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_auto_20200313_1610'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='description',
            field=models.TextField(blank=True, max_length=300, null=True),
        ),
    ]
