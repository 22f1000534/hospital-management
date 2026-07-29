from django.db import models

from common.models import BaseModel


class Qualification(BaseModel):
    code = models.CharField(
        max_length=20,
        unique=True,
    )

    name = models.CharField(
        max_length=255,
        unique=True,
    )

    description = models.TextField(
        blank=True,
    )

    is_active = models.BooleanField(
        default=True,
    )

    class Meta:
        ordering = ["code"]
        indexes = [
            models.Index(fields=["code"]),
            models.Index(fields=["name"]),
        ]

    def __str__(self):
        return self.code