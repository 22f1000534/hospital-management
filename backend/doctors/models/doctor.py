from django.conf import settings
from django.db import models
from django.utils import timezone

from common.models import BaseModel
from doctors.choices import Gender


class Doctor(BaseModel):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="doctor_profile",
    )

    medical_registration_number = models.CharField(
        max_length=100,
        unique=True,
    )

    gender = models.CharField(
        max_length=20,
        choices=Gender.choices,
    )

    date_of_birth = models.DateField(
        null=True,
        blank=True,
    )

    practice_started_on = models.DateField(
        null=True,
        blank=True,
    )

    bio = models.TextField(
        blank=True,
    )

    profile_picture = models.ImageField(
        upload_to="doctors/profile_pictures/",
        blank=True,
        null=True,
    )

    is_verified = models.BooleanField(
        default=False,
    )

    is_active = models.BooleanField(
        default=True,
    )

    class Meta:
        ordering = ["user__first_name"]
        indexes = [
            models.Index(fields=["medical_registration_number"]),
            models.Index(fields=["is_verified"]),
        ]

    @property
    def years_of_experience(self):
        if not self.practice_started_on:
            return None

        today = timezone.localdate()

        years = today.year - self.practice_started_on.year

        if (
            today.month,
            today.day,
        ) < (
            self.practice_started_on.month,
            self.practice_started_on.day,
        ):
            years -= 1

        return years

    def __str__(self):
        full_name = f"{self.user.first_name} {self.user.last_name}".strip()
        return full_name or self.user.email
