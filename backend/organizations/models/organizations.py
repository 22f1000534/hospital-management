from django.conf import settings
from django.db import models
from django.utils.text import slugify

from common.models import BaseModel
from organizations.choices import OrganizationType


class Organization(BaseModel):
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="organizations",
    )

    name = models.CharField(
        max_length=255,
    )

    slug = models.SlugField(
        unique=True,
        blank=True,
    )

    organization_type = models.CharField(
        max_length=30,
        choices=OrganizationType.choices,
    )

    description = models.TextField(
        blank=True,
    )

    phone_number = models.CharField(
        max_length=20,
    )

    email = models.EmailField()

    website = models.URLField(
        blank=True,
    )

    logo = models.ImageField(
        upload_to="organizations/logos/",
        blank=True,
        null=True,
    )

    address_line_1 = models.CharField(
        max_length=255,
    )

    address_line_2 = models.CharField(
        max_length=255,
        blank=True,
    )

    city = models.CharField(
        max_length=100,
    )

    state = models.CharField(
        max_length=100,
    )

    country = models.CharField(
        max_length=100,
        default="India",
    )

    postal_code = models.CharField(
        max_length=20,
    )

    is_verified = models.BooleanField(
        default=False,
    )

    is_active = models.BooleanField(
        default=True,
    )

    class Meta:
        ordering = ["name"]
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["city"]),
            models.Index(fields=["organization_type"]),
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
