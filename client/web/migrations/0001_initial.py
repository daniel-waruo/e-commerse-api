# Generated by Django 3.0.3 on 2020-02-18 07:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CarouselItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('caption', models.TextField()),
                ('url_to', models.URLField()),
                ('image_url', models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name='FeaturedProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='products.Product')),
            ],
        ),
    ]
