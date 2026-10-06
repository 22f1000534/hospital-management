from django.urls import path

from appointments.views import (
    AppointmentCancelView,
    AppointmentDetailView,
    AppointmentListCreateView,
)

urlpatterns = [
    path(
        "",
        AppointmentListCreateView.as_view(),
        name="appointment-list",
    ),
    path(
        "<uuid:pk>/",
        AppointmentDetailView.as_view(),
        name="appointment-detail",
    ),
    path(
        "<uuid:pk>/cancel/",
        AppointmentCancelView.as_view(),
        name="appointment-cancel",
    ),
]