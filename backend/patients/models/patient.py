from django.conf import settings
from django.db import models

from common.models import BaseModel
from patients.choices import BloodGroup, Gender


class Patient(BaseModel):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="patient_profile",
    )

    date_of_birth = models.DateField(
        null=True,
        blank=True,
    )

    gender = models.CharField(
        max_length=20,
        choices=Gender.choices,
        blank=True,
    )

    blood_group = models.CharField(
        max_length=3,
        choices=BloodGroup.choices,
        blank=True,
    )

    address_line_1 = models.CharField(
        max_length=255,
        blank=True,
    )

    address_line_2 = models.CharField(
        max_length=255,
        blank=True,
    )

    city = models.CharField(
        max_length=100,
        blank=True,
    )

    state = models.CharField(
        max_length=100,
        blank=True,
    )

    postal_code = models.CharField(
        max_length=20,
        blank=True,
    )

    country = models.CharField(
        max_length=100,
        default="India",
    )

    def __str__(self):
        return str(self.user)
