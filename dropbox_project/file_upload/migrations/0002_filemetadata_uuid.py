# Generated by Django 4.2.7 on 2023-11-18 05:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('file_upload', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='filemetadata',
            name='uuid',
            field=models.UUIDField(default=0),
        ),
    ]
