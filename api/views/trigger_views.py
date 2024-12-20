from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from api.models.trigger_models import ArchivedEvent, Event, EventLog

from api.serializers.trigger_serializers import (
    ArchivedEventSerializer,
    EventSerializer,
    EventLogSerializer,
)
from django.shortcuts import get_object_or_404
from tasks.event_log import handle_trigger_event
from rest_framework.permissions import IsAuthenticated


# Create your views here.
class EventListCreateView(generics.ListCreateAPIView):
    queryset = Event.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = EventSerializer

    def get(self, request):
        qs = self.get_queryset().filter(user=request.user)
        serializer = self.get_serializer(qs, many=True)
        return Response(data={"message": serializer.data})

    def post(self, request):
        payload = request.data

        is_test_trigger = payload.get("is_test_trigger", None)
        if payload.get("schedule_time") is None:
            payload["schedule_time"] = payload["start_time"]

        serializer = self.get_serializer(data=payload)
        serializer.is_valid(raise_exception=True)
        event_instance = serializer.save(user=request.user)
        if not is_test_trigger:
            is_recurring = payload.get("is_recurring", None)
            is_scheduled_trigger = payload.get("is_scheduled_trigger", None)

            if is_recurring or is_scheduled_trigger:
                """
                Logic for scheduled tasks
                write function call
                """
                schedule_time = payload.get("schedule_time")
                print(request.user)
                handle_trigger_event.apply_async(
                    (event_instance.id, "SCHEDULED", request.user.id), eta=schedule_time
                )
            else:
                event_log_data = {
                    "events": serializer.instance,
                    "event_type": "API",
                    "payload": payload,
                    "user": request.user.id,
                    "event_name": event_instance.name,
                }

                event_log = EventLogSerializer(data=event_log_data)
                event_log.is_valid(raise_exception=True)
                event_log.save()
                ## Delete from created event, since this is API it would be
                ## fired immediately and stored in EventLog

                event_instance.delete()
        else:
            ## Call the worker
            pass

        return Response(
            data={f"Trigger successfully created {serializer.data}"}, status=200
        )


class EventRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = EventSerializer

    def put(self, request, id=None):

        qs = self.get_queryset().filter(user=request.user)
        event = get_object_or_404(qs, id=id)

        serializer = self.get_serializer(event, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        instance = serializer.instance

        if instance.is_scheduled_trigger:
            schedule_time = instance.get("schedule_time")
            handle_trigger_event.apply_async(
                (event_instance.id, "SCHEDULED", request.user.id), eta=schedule_time
            )
        else:
            event_log_data = {
                "event": serializer.instance,
                "event_type": "API",
                "payload": payload,
                "user": request.user.id,
                "event_name": event_instance.name,
            }

            event_log = EventLogSerializer(data=event_log_data)
            event_log.is_valid(raise_exception=True)
            event_log.save()
            ## Delete from created event, since this is API it would be
            ## fired immediately and stored in EventLog

            instance.delete()

        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, id=None):
        qs = self.get_queryset().filter(user=request.user)
        event = get_object_or_404(qs, id=id)

        event_log = Eventlog.objects.filter(events=event)

        if event_log.exists():
            return Response(
                {"message": "Cannot delete the event since it is in process"},
                status=400,
            )

        event.delete()
        return Response({"message": "Event deleted!"}, status=200)


class EventLogList(generics.ListAPIView):
    queryset = EventLog.objects.exclude(is_archived=True)
    permission_classes = [IsAuthenticated]
    serializer_class = EventLogSerializer

    def get(self, request):
        qs = self.get_queryset().filter(user=request.user)
        serializer = self.get_serializer(qs, many=True)
        return Response(data={"message": serializer.data})


class ArchivedEventView(generics.ListAPIView):
    queryset = ArchivedEvent.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = ArchivedEventSerializer

    def get(self, request):
        qs = self.get_queryset()
        serializer = self.get_serializer(qs, many=True)
        return Response(data={"message": serializer.data})
