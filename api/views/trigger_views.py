from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from api.models.trigger_models import Event

from api.serializers.trigger_serializers import EventSerializer


# Create your views here.
class Event(generics.GenericAPIView):
    queryset = Event.objects.all()
    permission_classes = [AllowAny]
    serializer_class = EventSerializer

    def get(self, request):
        qs = self.get_queryset()
        serializer = self.get_serializer(qs, many=True)
        return Response(data={"message": serializer.data})

    def post(self, request):
        payload = request.data

        is_test_trigger = payload.get("is_test_trigger", None)
        if payload.get("schedule_time") is None:
            payload["schedule_time"] = payload["start_time"]

        if not is_test_trigger:
            serializer = self.get_serializer(data=payload)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            is_recurring = payload.get("is_recurring", None)

            if is_recurring:
                """
                Logic for scheduled tasks
                write function call
                """
                pass
        else:
            ## Call the worker
            pass

        return Response(
            data={f"Trigger successfully created {serializer.data}"}, status=200
        )
