# Generated by Django 4.2.6 on 2023-10-30 07:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0016_enrollment_delete_garima'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='discount',
        ),
        migrations.RemoveField(
            model_name='course',
            name='featured_videos',
        ),
        migrations.RemoveField(
            model_name='course',
            name='price',
        ),
    ]