from rest_framework import status
from rest_framework.generics import GenericAPIView, ListCreateAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from accounts.choices import UserRole
from accounts.permissions.roles import IsPatient
from appointments.models import Appointment
from appointments.permissions import CanAccessAppointment
from appointments.serializers import (
    AppointmentCancelSerializer,
    AppointmentCreateSerializer,
    AppointmentSerializer,
)


class AppointmentQuerysetMixin:
    def get_queryset(self):
        user = self.request.user

        queryset = Appointment.objects.select_related(
            "patient__user",
            "doctor_organization__doctor__user",
            "doctor_organization__organization",
            "doctor_organization__department",
        )

        if user.role == UserRole.SUPER_ADMIN:
            return queryset

        if user.role == UserRole.PATIENT:
            return queryset.filter(patient__user=user)

        if user.role == UserRole.DOCTOR:
            return queryset.filter(
                doctor_organization__doctor__user=user,
            )

        if user.role == UserRole.ORG_ADMIN:
            return queryset.filter(
                doctor_organization__organization__memberships__user=user,
                doctor_organization__organization__memberships__is_active=True,
            ).distinct()

        return queryset.none()


class AppointmentListCreateView(
    AppointmentQuerysetMixin,
    ListCreateAPIView,
):
    serializer_class = AppointmentSerializer

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsPatient()]

        return [IsAuthenticated()]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return AppointmentCreateSerializer

        return AppointmentSerializer

    def perform_create(self, serializer):
        serializer.save(patient=self.request.user.patient_profile)

class AppointmentDetailView(
    AppointmentQuerysetMixin,
    RetrieveAPIView,
):
    serializer_class = AppointmentSerializer
    permission_classes = [
        IsAuthenticated,
        CanAccessAppointment,
    ]


class AppointmentCancelView(
    AppointmentQuerysetMixin,
    GenericAPIView,
):
    serializer_class = AppointmentCancelSerializer
    permission_classes = [
        IsPatient,
        CanAccessAppointment,
    ]

    def post(self, request, *args, **kwargs):
        appointment = self.get_object()

        serializer = self.get_serializer(
            appointment,
            data=request.data,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            AppointmentSerializer(appointment).data,
            status=status.HTTP_200_OK,
        )