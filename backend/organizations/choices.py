from django.db import models

class OrganizationType(models.TextChoices):
    HOSPITAL = "HOSPITAL", "Hospital"
    CLINIC = "CLINIC", "Clinic"
    DIAGNOSTIC_CENTER = "DIAGNOSTIC_CENTER", "Diagnostic Center"
    MEDICAL_CENTER = "MEDICAL_CENTER", "Medical Center"