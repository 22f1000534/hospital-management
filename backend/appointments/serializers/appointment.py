from rest_framework import serializers

from appointments.models import Appointment


class AppointmentSerializer(serializers.ModelSerializer):
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
            "created_at",
            "updated_at",
        ]