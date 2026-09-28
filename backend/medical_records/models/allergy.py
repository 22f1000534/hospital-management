from django.db import models

from common.models import BaseModel
from doctors.models import Doctor
from medical_records.choices import (
    AllergySeverity,
    AllergyStatus,
    AllergyType,
)
from patients.models import Patient


class Allergy(BaseModel):
    patient = models.ForeignKey(
        Patient,
        on_delete=models.PROTECT,
        related_name="allergies",
    )

    allergen = models.CharField(
        max_length=255,
    )

    allergy_type = models.CharField(
        max_length=20,
        choices=AllergyType.choices,
    )

    reaction = models.CharField(
        max_length=255,
    )

    severity = models.CharField(
        max_length=20,
        choices=AllergySeverity.choices,
        default=AllergySeverity.UNKNOWN,
    )

    status = models.CharField(
        max_length=20,
        choices=AllergyStatus.choices,
        default=AllergyStatus.ACTIVE,
    )

    notes = models.TextField(
        blank=True,
    )

    recorded_by = models.ForeignKey(
        Doctor,
        on_delete=models.PROTECT,
        related_name="recorded_allergies",
    )

    class Meta:
        ordering = ["allergen"]
        indexes = [
            models.Index(fields=["patient", "status"]),
            models.Index(fields=["patient", "allergy_type"]),
        ]

    def __str__(self):
        return f"{self.allergen} - {self.patient}"
