from django.db import models

from common.models import BaseModel
from doctors.models.doctor import Doctor
from master.models import Department
from organizations.models import Organization


class DoctorOrganization(BaseModel):
    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.CASCADE,
        related_name="organization_assignments",
    )
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="doctor_assignments",
    )
    department = models.ForeignKey(
        Department,
        on_delete=models.PROTECT,
        related_name="doctor_organizations",
    )
    consultation_fee = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
    )
    joined_on = models.DateField()
    left_on = models.DateField(
        null=True,
        blank=True,
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["organization__name", "doctor__user__first_name"]
        constraints = [
            models.UniqueConstraint(
                fields=["doctor", "organization", "department"],
                name="unique_doctor_organization_department",
            ),
        ]
        indexes = [
            models.Index(fields=["doctor", "organization"]),
            models.Index(fields=["organization", "department"]),
        ]

    def __str__(self):
        return f"{self.doctor} - " f"{self.organization} - " f"{self.department}"
