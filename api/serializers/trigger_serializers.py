from rest_framework.serializers import ModelSerializer
from api.models.trigger_models import ArchivedEvent, Event, EventLog
from rest_framework import serializers
from django.utils import timezone


class EventSerializer(ModelSerializer):
    class Meta:
        model = Event
        fields = "__all__"

    def validate(self, attrs):
        is_scheduled_trigger = attrs.get("is_scheduled_trigger")
        start_time = attrs.get("start_time")
        schedule_time = attrs.get("schedule_time")
        is_recurring = attrs.get("is_recurring")
        recurring_minutes = attrs.get("recurring_minutes")
        payload = attrs.get("payload")
        is_test_trigger = attrs.get("is_test_trigger")

        # Validate common fields
        if not start_time:
            raise serializers.ValidationError({"start_time": "Start time is required."})

        # Ensure start_time is in the future
        if start_time <= timezone.now():
            raise serializers.ValidationError(
                {"start_time": "Start time must be in the future."}
            )

        # Validate Scheduled Triggers
        if is_scheduled_trigger:
            if is_recurring and (recurring_minutes is None or recurring_minutes <= 0):
                raise serializers.ValidationError(
                    {
                        "recurring_minutes": "Recurring minutes must be provided and greater than zero for recurring triggers."
                    }
                )
            if payload is not None:
                raise serializers.ValidationError(
                    {"payload": "Payload is not allowed for scheduled triggers."}
                )

        # Validate API Triggers
        if not is_scheduled_trigger:
            if is_recurring or recurring_minutes:
                raise serializers.ValidationError(
                    {
                        "non_field_errors": "API triggers cannot have recurring_minutes, or is_recurring set."
                    }
                )
            if not payload:
                raise serializers.ValidationError(
                    {"payload": "Payload is required for API triggers."}
                )

        # Validate Test Triggers
        if is_test_trigger and not is_scheduled_trigger:
            if is_recurring or recurring_minutes:
                raise serializers.ValidationError(
                    {
                        "non_field_errors": "Test API triggers cannot have recurring_minutes, or is_recurring set."
                    }
                )

            if not payload:
                raise serializers.ValidationError(
                    {"payload": "Payload is required for API triggers."}
                )

        return attrs


class EventLogSerializer(ModelSerializer):
    event_name = serializers.CharField(source="events.name")

    class Meta:
        model = EventLog
        fields = "__all__"
        extra_fields = ["event_name"]


class ArchivedEventSerializer(ModelSerializer):
    event_log_name = serializers.CharField(source="original_event.events.name")

    class Meta:
        model = ArchivedEvent
        fields = "__all__"
        extra_fields = ["event_log_name"]
