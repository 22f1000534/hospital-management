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


class AllergyType(models.TextChoices):
    DRUG = "DRUG", "Drug"
    FOOD = "FOOD", "Food"
    ENVIRONMENTAL = "ENVIRONMENTAL", "Environmental"
    CONTACT = "CONTACT", "Contact"
    OTHER = "OTHER", "Other"


class AllergySeverity(models.TextChoices):
    MILD = "MILD", "Mild"
    MODERATE = "MODERATE", "Moderate"
    SEVERE = "SEVERE", "Severe"
    LIFE_THREATENING = "LIFE_THREATENING", "Life Threatening"
    UNKNOWN = "UNKNOWN", "Unknown"


class AllergyStatus(models.TextChoices):
    ACTIVE = "ACTIVE", "Active"
    INACTIVE = "INACTIVE", "Inactive"
    UNKNOWN = "UNKNOWN", "Unknown"
