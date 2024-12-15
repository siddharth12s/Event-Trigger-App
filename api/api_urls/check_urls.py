from django.urls import path, include
from api.views.trigger_views import (
    ArchivedEventView,
    EventListCreateView,
    EventLogList,
    EventRetrieveUpdateDeleteView,
)

url_patterns = [
    path("events", EventListCreateView.as_view()),
    path("events/<int:id>", EventRetrieveUpdateDeleteView.as_view()),
    path("event-log", EventLogList.as_view()),
    path("archived-events", ArchivedEventView.as_view()),
]
