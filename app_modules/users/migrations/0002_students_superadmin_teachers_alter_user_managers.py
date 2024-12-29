# Generated by Django 5.1.3 on 2024-11-20 10:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Students',
            fields=[
            ],
            options={
                'verbose_name': 'Student',
                'verbose_name_plural': 'Students',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('users.user',),
        ),
        migrations.CreateModel(
            name='SuperAdmin',
            fields=[
            ],
            options={
                'verbose_name': 'SuperAdmin',
                'verbose_name_plural': 'SuperAdmins',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('users.user',),
        ),
        migrations.CreateModel(
            name='Teachers',
            fields=[
            ],
            options={
                'verbose_name': 'Teacher',
                'verbose_name_plural': 'Teachers',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('users.user',),
        ),
        migrations.AlterModelManagers(
            name='user',
            managers=[
            ],
        ),
    ]
