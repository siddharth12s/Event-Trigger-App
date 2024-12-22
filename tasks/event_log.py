from celery import shared_task
from django.utils.timezone import now
from api.models.trigger_models import EventLog, Event, ArchivedEvent
from datetime import datetime, timedelta
from django.db import transaction
import logging

logger = logging.getLogger("celery")

from api.models.user_models import User


@shared_task
def handle_trigger_event(trigger_id, event_type, user_id):

    logger.info(
        f"Task started: trigger_id={trigger_id}, event_type={event_type}, user_id={user_id}"
    )
    try:
        event = Event.objects.get(id=trigger_id)
        user = User.objects.get(id=user_id)

        if event.has_expired():
            return

        EventLog.objects.create(
            events=event,
            event_type=event_type,
            timestamp=now(),
            payload=event.payload,
            is_test=True if event.is_test_trigger else False,
            user=user,
        )

        """
            For updating the new scheduled time
        """
        if event.is_recurring:
            recurring_minutes = event.recurring_minutes
            new_time = event.schedule_time + timedelta(minutes=recurring_minutes)

            event.schedule_time = new_time
            event.save()

            handle_trigger_event.apply_async(
                (event.id, event_type, user_id), eta=new_time
            )
    except Event.DoesNotExist:
        pass


@shared_task
def archive_old_events():
    # Archive events older than 5 minutes
    # Change the minutes to 48 * 60 = 2880 minutes
    cutoff_date = now() - timedelta(minutes=5)
    old_logs = EventLog.objects.filter(timestamp__lt=cutoff_date, is_archived=False)
    print(old_logs)
    with transaction.atomic():
        for log in old_logs:
            ArchivedEvent.objects.create(original_event=log, archived_at=now())
            log.is_archived = True
            log.save()


@shared_task
def delete_expired_events():
    cutoff_time = now()
    event_log_cutoff_time = cutoff_time - timedelta(minutes=5)
    archived_event_cutoff_time = cutoff_time - timedelta(minutes=15)

    events = Event.objects.filter(expiry_time__lt=cutoff_time)

    for event in events:
        try:
            event_logs = EventLog.objects.filter(
                events=event, timestamp__lt=event_log_cutoff_time, is_archived=True
            )
            event_logs.delete()

            archived_events = ArchivedEvent.objects.filter(
                original_event__events=event, archived_at__lt=archived_event_cutoff_time
            )
            archived_events.delete()

            if (
                not EventLog.objects.filter(events=event).exists()
                and not ArchivedEvent.objects.filter(
                    original_event__events=event
                ).exists()
            ):
                event.delete()
                print(
                    f"Deleted Event: {event.name} and its associated logs and archives."
                )

        except Exception as e:
            print(f"Failed to delete Event: {event.name}. Error: {str(e)}")
