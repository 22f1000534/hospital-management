from django.db import models

from common.models import BaseModel
from treatments.choices import PrescriptionStatus

from .treatment import Treatment


class Prescription(BaseModel):
    treatment = models.ForeignKey(
        Treatment,
        on_delete=models.PROTECT,
        related_name="prescriptions",
    )
    medication_name = models.CharField(max_length=255)
    dosage = models.CharField(max_length=100)
    frequency = models.CharField(max_length=100)
    route = models.CharField(max_length=50, blank=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    instructions = models.TextField(blank=True)
    status = models.CharField(
        max_length=20,
        choices=PrescriptionStatus.choices,
        default=PrescriptionStatus.ACTIVE,
    )

    class Meta:
        ordering = ["-start_date", "-created_at"]

    def __str__(self):
        return f"{self.medication_name} - {self.treatment}"
