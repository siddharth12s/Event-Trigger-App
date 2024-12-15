from celery import shared_task
from django.utils.timezone import now
from api.models.trigger_models import EventLog, Event, ArchivedEvent
from datetime import datetime, timedelta
from django.db import transaction


@shared_task
def handle_trigger_event(trigger_id, event_type):
    try:
        event = Event.objects.get(id=trigger_id)
        EventLog.objects.create(
            event=event,
            event_type=event_type,
            timestamp=now(),
            payload=event.payload,
            is_test=True if event.is_test_trigger else False,
        )

        """
            For updating the new scheduled time
        """
        if event.is_recurring:
            recurring_minutes = event.recurring_minutes
            new_time = event.schedule_time + timedelta(minutes=recurring_minutes)

            event.schedule_time = new_time
            event.save()

            handle_trigger_event.apply_async((event.id, event_type), eta=new_time)
    except Event.DoesNotExist:
        pass


@shared_task
def archive_old_events():
    # Archive events older than 5 minutes
    cutoff_date = now() - timedelta(minutes=5)
    old_logs = EventLog.objects.filter(timestamp__lt=cutoff_date)
    print(old_logs)
    with transaction.atomic():
        for log in old_logs:
            ArchivedEvent.objects.create(original_event=log, archived_at=now())
            log.is_archived = True
            log.save()
