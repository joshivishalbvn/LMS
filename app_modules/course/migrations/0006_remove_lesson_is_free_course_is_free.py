# Generated by Django 5.1.3 on 2024-12-04 10:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0005_lesson_is_free'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lesson',
            name='is_free',
        ),
        migrations.AddField(
            model_name='course',
            name='is_free',
            field=models.BooleanField(default=True),
        ),
    ]
