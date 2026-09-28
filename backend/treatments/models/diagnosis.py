from datetime import date

from django.db import models

from common.models import BaseModel
from consultations.models import Consultation
from treatments.choices import DiagnosisType


class Diagnosis(BaseModel):
    consultation = models.ForeignKey(
        Consultation,
        on_delete=models.PROTECT,
        related_name="diagnoses",
    )
    condition = models.CharField(max_length=255)
    diagnosis_type = models.CharField(
        max_length=20,
        choices=DiagnosisType.choices,
    )
    diagnosed_on = models.DateField(default=date.today)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["-diagnosed_on", "-created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["consultation"],
                condition=models.Q(diagnosis_type="PRIMARY"),
                name="unique_primary_diagnosis_per_consultation",
            ),
        ]

    def __str__(self):
        return f"{self.condition} - {self.consultation}"