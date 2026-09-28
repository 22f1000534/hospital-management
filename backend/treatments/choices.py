from django.db import models


class DiagnosisType(models.TextChoices):
    PRIMARY = "PRIMARY", "Primary"
    SECONDARY = "SECONDARY", "Secondary"
    PROVISIONAL = "PROVISIONAL", "Provisional"


class TreatmentType(models.TextChoices):
    MEDICATION = "MEDICATION", "Medication"
    PHYSIOTHERAPY = "PHYSIOTHERAPY", "Physiotherapy"
    PROCEDURE = "PROCEDURE", "Procedure"
    SURGERY = "SURGERY", "Surgery"
    LIFESTYLE = "LIFESTYLE", "Lifestyle"
    DIET = "DIET", "Diet"
    OTHER = "OTHER", "Other"


class TreatmentStatus(models.TextChoices):
    PLANNED = "PLANNED", "Planned"
    ONGOING = "ONGOING", "Ongoing"
    COMPLETED = "COMPLETED", "Completed"
    DISCONTINUED = "DISCONTINUED", "Discontinued"


class PrescriptionStatus(models.TextChoices):
    ACTIVE = "ACTIVE", "Active"
    COMPLETED = "COMPLETED", "Completed"
    DISCONTINUED = "DISCONTINUED", "Discontinued"