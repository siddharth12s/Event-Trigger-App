# Generated by Django 5.1.4 on 2024-12-20 22:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_event_user_eventlog_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='expiry_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
