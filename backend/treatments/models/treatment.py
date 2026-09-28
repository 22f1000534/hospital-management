from django.db import models

from common.models import BaseModel
from consultations.models import Consultation
from treatments.choices import TreatmentStatus, TreatmentType

from .diagnosis import Diagnosis


class Treatment(BaseModel):
    consultation = models.ForeignKey(
        Consultation,
        on_delete=models.PROTECT,
        related_name="treatments",
    )
    diagnoses = models.ManyToManyField(
        Diagnosis,
        related_name="treatments",
        blank=True,
    )
    treatment_type = models.CharField(
        max_length=20,
        choices=TreatmentType.choices,
    )
    description = models.TextField()
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=TreatmentStatus.choices,
        default=TreatmentStatus.PLANNED,
    )
    instructions = models.TextField(blank=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.treatment_type} - {self.consultation}"
