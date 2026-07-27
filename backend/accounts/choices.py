from django.db import models


class UserRole(models.TextChoices):
    PATIENT = "PATIENT", "Patient"
    DOCTOR = "DOCTOR", "Doctor"
    ORG_ADMIN = "ORG_ADMIN", "Organization Admin"
    SUPER_ADMIN = "SUPER_ADMIN", "Super Admin"