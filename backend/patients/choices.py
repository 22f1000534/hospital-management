from django.db import models

class Gender(models.TextChoices):
    MALE = "MALE", "Male"
    FEMALE = "FEMALE", "Female"
    OTHER = "OTHER", "Other"
    PREFER_NOT_TO_SAY = "PREFER_NOT_TO_SAY", "Prefer not to say"

class BloodGroup(models.TextChoices):
    A_POSITIVE = "A+", "A+"
    A_NEGATIVE = "A-", "A-"
    B_POSITIVE = "B+", "B+"
    B_NEGATIVE = "B-", "B-"
    AB_POSITIVE = "AB+", "AB+"
    AB_NEGATIVE = "AB-", "AB-"
    O_POSITIVE = "O+", "O+"
    O_NEGATIVE = "O-", "O-"

class EmergencyContactRelationship(models.TextChoices):
    PARENT = "PARENT", "Parent"
    SPOUSE = "SPOUSE", "Spouse"
    SIBLING = "SIBLING", "Sibling"
    CHILD = "CHILD", "Child"
    RELATIVE = "RELATIVE", "Relative"
    FRIEND = "FRIEND", "Friend"
    OTHER = "OTHER", "Other"