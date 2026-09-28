from django.db import models


class DiagnosisType(models.TextChoices):
    PRIMARY = "PRIMARY", "Primary"
    SECONDARY = "SECONDARY", "Secondary"
    PROVISIONAL = "PROVISIONAL", "Provisional"