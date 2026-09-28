from django.db import models

from common.models import BaseModel


class Language(BaseModel):
    name = models.CharField(
        max_length=50,
        unique=True,
    )

    code = models.CharField(
        max_length=10,
        unique=True,
    )

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name
