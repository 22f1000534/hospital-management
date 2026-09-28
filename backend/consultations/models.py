from django.db import models

from appointments.models import Appointment
from common.models import BaseModel

from .choices import ConsultationStatus


class Consultation(BaseModel):
    appointment = models.OneToOneField(
        Appointment,
        on_delete=models.PROTECT,
        related_name="consultation",
    )
    chief_complaint = models.TextField()
    history_of_present_illness = models.TextField(blank=True)
    examination_notes = models.TextField(blank=True)
    clinical_notes = models.TextField(blank=True)
    doctor_notes = models.TextField(blank=True)
    status = models.CharField(
        max_length=20,
        choices=ConsultationStatus.choices,
        default=ConsultationStatus.IN_PROGRESS,
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Consultation - {self.appointment}"
