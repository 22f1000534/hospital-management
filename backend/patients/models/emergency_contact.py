from django.db import models

from common.models import BaseModel
from patients.choices import EmergencyContactRelationship

from .patient import Patient


class EmergencyContact(BaseModel):
    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name="emergency_contacts",
    )

    name = models.CharField(
        max_length=100,
    )

    relationship = models.CharField(
        max_length=20,
        choices=EmergencyContactRelationship.choices,
    )

    phone_number = models.CharField(
        max_length=20,
    )

    is_primary = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return f"{self.name} - {self.patient}"
