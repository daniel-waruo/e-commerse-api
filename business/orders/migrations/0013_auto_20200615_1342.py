# Generated by Django 3.0.7 on 2020-06-15 13:42

from django.db import migrations, models
import django.db.models.deletion
import shortuuidfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_category_description'),
        ('orders', '0012_auto_20200605_1447'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='id',
            field=shortuuidfield.fields.ShortUUIDField(blank=True, default='nyXe9wkVvSQtjGbiP7pbSf', editable=False, max_length=22, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='productorder',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='orders', to='products.Product'),
        ),
        migrations.AlterField(
            model_name='sendydeliveryinfo',
            name='order',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='sendy_info', to='orders.Order'),
        ),
    ]
