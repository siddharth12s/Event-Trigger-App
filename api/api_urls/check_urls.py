from django.urls import path, include
from api.views.trigger_views import Event

url_patterns = [path("events", Event.as_view())]
