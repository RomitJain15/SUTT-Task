# Generated by Django 5.0.2 on 2024-03-01 21:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_alter_trip_destination_delete_location'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='group',
            name='members',
        ),
        migrations.AddField(
            model_name='group',
            name='members',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
