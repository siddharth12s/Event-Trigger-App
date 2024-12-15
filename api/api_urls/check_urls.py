from django.urls import path, include
from api.views.trigger_views import (
    ArchivedEventView,
    EventListCreateView,
    EventLogList,
    EventRetrieveUpdateDeleteView,
)
from api.views.user_views import CustomTokenObtainPairView, UserCreateView

url_patterns = [
    path("events", EventListCreateView.as_view()),
    path("events/<int:id>", EventRetrieveUpdateDeleteView.as_view()),
    path("event-log", EventLogList.as_view()),
    path("archived-events", ArchivedEventView.as_view()),
    path("user", UserCreateView.as_view()),
    path("login", CustomTokenObtainPairView.as_view()),
]
