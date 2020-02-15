# Generated by Django 3.0.2 on 2020-01-25 09:27

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('app_label', models.CharField(editable=False, max_length=100)),
                ('name', models.CharField(max_length=100, null=True)),
            ],
            options={
                'verbose_name': 'Department',
                'permissions': (('add_staff', 'Can add staff to a department'), ('set_permissions', 'Set permissions of a Departmental staff'), ('include_department', "Add a department to a staff's access"), ('manage_department_manager', 'Manage the access of a Departmental Manager'), ('edit_departments', 'Can edit the name of a Department'), ('manage_general_manager', 'Manage the access of a General Manager')),
            },
        ),
    ]
