from django.db import models

from common.models import BaseModel
from doctors.models import DoctorOrganization
from appointments.choices import AppointmentStatus
from patients.models import Patient


class Appointment(BaseModel):
    patient = models.ForeignKey(
        Patient,
        on_delete=models.PROTECT,
        related_name="appointments",
    )

    doctor_organization = models.ForeignKey(
        DoctorOrganization,
        on_delete=models.PROTECT,
        related_name="appointments",
    )

    appointment_date = models.DateField()

    start_time = models.TimeField()

    end_time = models.TimeField()

    status = models.CharField(
        max_length=20,
        choices=AppointmentStatus.choices,
        default=AppointmentStatus.PENDING,
    )

    reason = models.TextField(
        blank=True,
    )

    notes = models.TextField(
        blank=True,
    )

    cancellation_reason = models.TextField(
        blank=True,
    )

    class Meta:
        ordering = [
            "appointment_date",
            "start_time",
        ]
        indexes = [
            models.Index(
                fields=["doctor_organization", "appointment_date"],
            ),
            models.Index(
                fields=["patient", "appointment_date"],
            ),
            models.Index(
                fields=["status"],
            ),
        ]

    def __str__(self):
        return (
            f"{self.patient} - "
            f"{self.doctor_organization} - "
            f"{self.appointment_date} "
            f"{self.start_time}"
        )