from django.db import models

from common.models import BaseModel
from doctors.models import Doctor
from medical_records.choices import HistoryStatus, HistoryType
from patients.models import Patient


class MedicalHistory(BaseModel):
    patient = models.ForeignKey(
        Patient,
        on_delete=models.PROTECT,
        related_name="medical_histories",
    )

    condition = models.CharField(
        max_length=255,
    )

    history_type = models.CharField(
        max_length=30,
        choices=HistoryType.choices,
    )

    diagnosed_on = models.DateField(
        null=True,
        blank=True,
    )

    resolved_on = models.DateField(
        null=True,
        blank=True,
    )

    status = models.CharField(
        max_length=20,
        choices=HistoryStatus.choices,
        default=HistoryStatus.ACTIVE,
    )

    notes = models.TextField(
        blank=True,
    )

    recorded_by = models.ForeignKey(
        Doctor,
        on_delete=models.PROTECT,
        related_name="recorded_medical_histories",
    )

    class Meta:
        ordering = ["-diagnosed_on", "-created_at"]
        indexes = [
            models.Index(fields=["patient", "status"]),
            models.Index(fields=["patient", "history_type"]),
        ]

    def __str__(self):
        return f"{self.condition} - {self.patient}"
