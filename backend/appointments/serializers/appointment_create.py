from rest_framework import serializers

from appointments.choices import AppointmentStatus
from appointments.models import Appointment


class AppointmentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = [
            "id",
            "patient",
            "doctor_organization",
            "appointment_date",
            "start_time",
            "end_time",
            "status",
            "reason",
            "notes",
            "cancellation_reason",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "patient",
            "status",
            "notes",
            "cancellation_reason",
            "created_at",
            "updated_at",
        ]

    def validate_doctor_organization(self, value):
        if not value.is_active:
            raise serializers.ValidationError(
                "This doctor is not currently available at this organization."
            )

        return value

    def validate(self, attrs):
        start_time = attrs.get("start_time")
        end_time = attrs.get("end_time")
        appointment_date = attrs.get("appointment_date")
        doctor_organization = attrs.get("doctor_organization")

        if start_time and end_time and end_time <= start_time:
            raise serializers.ValidationError(
                {"end_time": "End time must be after start time."}
            )

        if (
            appointment_date
            and start_time
            and end_time
            and doctor_organization
        ):
            overlapping_appointments = Appointment.objects.filter(
                doctor_organization=doctor_organization,
                appointment_date=appointment_date,
                start_time__lt=end_time,
                end_time__gt=start_time,
            ).exclude(status=AppointmentStatus.CANCELLED)

            if overlapping_appointments.exists():
                raise serializers.ValidationError(
                    "The selected time overlaps with an existing appointment."
                )

        return attrs