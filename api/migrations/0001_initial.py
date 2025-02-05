# Generated by Django 5.1.4 on 2024-12-14 19:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TimeStamp',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('timestamp_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='api.timestamp')),
                ('name', models.CharField(max_length=255)),
                ('is_scheduled_trigger', models.BooleanField(default=False)),
                ('start_time', models.DateTimeField()),
                ('schedule_time', models.DateTimeField(blank=True, null=True)),
                ('is_recurring', models.BooleanField(default=False)),
                ('recurring_minutes', models.IntegerField(blank=True, null=True)),
                ('payload', models.JSONField(blank=True, null=True)),
                ('is_test_trigger', models.BooleanField(default=False)),
            ],
            bases=('api.timestamp',),
        ),
        migrations.CreateModel(
            name='EventLog',
            fields=[
                ('timestamp_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='api.timestamp')),
                ('event_type', models.CharField(choices=[('SCHEDULED', 'SCHEDULED'), ('API', 'API')], max_length=255)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('payload', models.JSONField(blank=True, null=True)),
                ('is_test', models.BooleanField(default=False)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.event')),
            ],
            bases=('api.timestamp',),
        ),
        migrations.CreateModel(
            name='ArchivedEvent',
            fields=[
                ('timestamp_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='api.timestamp')),
                ('archived_at', models.DateTimeField(auto_now_add=True)),
                ('original_event', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='api.eventlog')),
            ],
            bases=('api.timestamp',),
        ),
    ]
