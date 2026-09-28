from django.db import models


class Gender(models.TextChoices):
    MALE = "MALE", "Male"
    FEMALE = "FEMALE", "Female"
    OTHER = "OTHER", "Other"
    PREFER_NOT_TO_SAY = "PREFER_NOT_TO_SAY", "Prefer not to say"
