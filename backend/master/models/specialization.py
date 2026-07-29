from django.db import models

from common.models import BaseModel

from .department import Department


class Specialization(BaseModel):
    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name="specializations",
    )

    name = models.CharField(
        max_length=100,
        unique=True,
    )

    description = models.TextField(
        blank=True,
    )

    is_active = models.BooleanField(
        default=True,
    )

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name