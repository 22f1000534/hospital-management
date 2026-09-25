from django.db import models

from django.db import models


class HistoryType(models.TextChoices):
    CHRONIC_CONDITION = "CHRONIC_CONDITION", "Chronic Condition"
    ACUTE_ILLNESS = "ACUTE_ILLNESS", "Acute Illness"
    SURGERY = "SURGERY", "Surgery"
    INJURY = "INJURY", "Injury"
    HOSPITALIZATION = "HOSPITALIZATION", "Hospitalization"
    OTHER = "OTHER", "Other"


class HistoryStatus(models.TextChoices):
    ACTIVE = "ACTIVE", "Active"
    RESOLVED = "RESOLVED", "Resolved"
    IN_REMISSION = "IN_REMISSION", "In Remission"
    UNKNOWN = "UNKNOWN", "Unknown"