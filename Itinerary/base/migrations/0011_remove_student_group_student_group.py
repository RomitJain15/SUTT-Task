# Generated by Django 5.0.2 on 2024-03-21 21:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0010_event_trip'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='group',
        ),
        migrations.AddField(
            model_name='student',
            name='group',
            field=models.ManyToManyField(to='base.group'),
        ),
    ]
