# Generated by Django 5.1.4 on 2024-12-15 11:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventlog',
            name='is_archived',
            field=models.BooleanField(default=False),
        ),
    ]
