# Generated by Django 5.0.2 on 2024-03-01 16:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_remove_trip_location'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trip',
            name='destination',
            field=models.CharField(max_length=100),
        ),
        migrations.DeleteModel(
            name='Location',
        ),
    ]