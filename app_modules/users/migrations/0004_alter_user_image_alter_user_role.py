# Generated by Django 5.1.3 on 2024-11-20 10:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_user_image_alter_user_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='users/profile pic/'),
        ),
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(blank=True, choices=[('Super Admin', 'Super Admin'), ('Teacher', 'Teacher'), ('Student', 'Student')], max_length=100, null=True, verbose_name='Role'),
        ),
    ]
