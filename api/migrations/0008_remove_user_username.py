# Generated by Django 5.1.4 on 2024-12-15 20:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_alter_user_username'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='username',
        ),
    ]
