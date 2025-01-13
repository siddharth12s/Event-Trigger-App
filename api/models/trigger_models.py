from django.db import models
from api.models.base_models import TimeStamp
from api.models.user_models import User
from datetime import timedelta
from django.utils import timezone


class Event(TimeStamp):
    name = models.CharField(max_length=255)
    is_scheduled_trigger = models.BooleanField(default=False)
    start_time = models.DateTimeField()
    schedule_time = models.DateTimeField(null=True, blank=True)
    is_recurring = models.BooleanField(default=False)
    recurring_minutes = models.IntegerField(null=True, blank=True)
    payload = models.JSONField(null=True, blank=True)
    is_test_trigger = models.BooleanField(default=False)
    user = models.ForeignKey(
        User, on_delete=models.PROTECT, null=True, related_name="events"
    )
    expiry_time = models.DateTimeField(null=True, blank=True, default=None)

    def save(self, *args, **kwargs):
        if self.schedule_time and not self.expiry_time:
            self.expiry_time = self.schedule_time + timedelta(hours=2)
        super().save(*args, **kwargs)

    def has_expired(self):
        return self.expiry_time <= timezone.now()


class EventLog(TimeStamp):
    EVENT_TYPE_CHOICES = [("SCHEDULED", "SCHEDULED"), ("API", "API")]
    events = models.ForeignKey(Event, on_delete=models.CASCADE)
    event_type = models.CharField(max_length=255, choices=EVENT_TYPE_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)
    payload = models.JSONField(null=True, blank=True)
    is_test = models.BooleanField(default=False)
    is_archived = models.BooleanField(default=False)
    user = models.ForeignKey(
        User, on_delete=models.PROTECT, null=True, related_name="event_logs"
    )

    class Meta:
        db_table = "event_log"
        verbose_name = "event_log"


class ArchivedEvent(TimeStamp):
    original_event = models.ForeignKey(EventLog, on_delete=models.CASCADE)
    archived_at = models.DateTimeField(auto_now_add=True)
