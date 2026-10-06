from datetime import datetime

from django.utils import timezone
from rest_framework import serializers

from appointments.choices import AppointmentStatus
from appointments.models import Appointment


class AppointmentCancelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ["cancellation_reason"]

    def validate_cancellation_reason(self, value):
        if not value.strip():
            raise serializers.ValidationError(
                "Cancellation reason cannot be empty."
            )
        return value

    def validate(self, attrs):
        appointment = self.instance

        if appointment.status == AppointmentStatus.CANCELLED:
            raise serializers.ValidationError(
                "This appointment is already cancelled."
            )

        if appointment.status in [
            AppointmentStatus.COMPLETED,
            AppointmentStatus.NO_SHOW,
        ]:
            raise serializers.ValidationError(
                "This appointment can no longer be cancelled."
            )

        appointment_start = datetime.combine(
            appointment.appointment_date,
            appointment.start_time,
        )
        appointment_start = timezone.make_aware(
            appointment_start,
            timezone.get_current_timezone(),
        )

        if timezone.now() >= appointment_start:
            raise serializers.ValidationError(
                "An appointment cannot be cancelled after it has started."
            )

        return attrs

    def update(self, instance, validated_data):
        instance.status = AppointmentStatus.CANCELLED
        instance.cancellation_reason = validated_data["cancellation_reason"]
        instance.save(
            update_fields=[
                "status",
                "cancellation_reason",
                "updated_at",
            ]
        )
        return instance