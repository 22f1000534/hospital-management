from datetime import date

import pytest
from django.db.models.deletion import ProtectedError

from accounts.models import User
from doctors.models import Doctor
from medical_records.models import Allergy
from patients.models import Patient


@pytest.mark.django_db
def test_create_allergy():
    doctor_user = User.objects.create_user(
        email="doctor@example.com",
        password="testpassword123",
        first_name="Anil",
        last_name="Kumar",
    )

    doctor = Doctor.objects.create(
        user=doctor_user,
        medical_registration_number="MED123456",
        gender="MALE",
    )

    patient_user = User.objects.create_user(
        email="patient@example.com",
        password="testpassword123",
        first_name="Rahul",
        last_name="Menon",
    )

    patient = Patient.objects.create(
        user=patient_user,
        date_of_birth=date(1995, 5, 15),
        gender="MALE",
    )

    allergy = Allergy.objects.create(
        patient=patient,
        allergen="Penicillin",
        allergy_type="DRUG",
        reaction="Skin rash",
        severity="SEVERE",
        status="ACTIVE",
        notes="Previous reaction to penicillin.",
        recorded_by=doctor,
    )

    assert allergy.patient == patient
    assert allergy.recorded_by == doctor
    assert allergy.allergen == "Penicillin"
    assert allergy.allergy_type == "DRUG"
    assert allergy.reaction == "Skin rash"
    assert allergy.severity == "SEVERE"
    assert allergy.status == "ACTIVE"


@pytest.mark.django_db
def test_allergy_defaults():
    doctor_user = User.objects.create_user(
        email="doctor@example.com",
        password="testpassword123",
        first_name="Anil",
        last_name="Kumar",
    )

    doctor = Doctor.objects.create(
        user=doctor_user,
        medical_registration_number="MED123457",
        gender="MALE",
    )

    patient_user = User.objects.create_user(
        email="patient@example.com",
        password="testpassword123",
        first_name="Rahul",
        last_name="Menon",
    )

    patient = Patient.objects.create(
        user=patient_user,
        date_of_birth=date(1995, 5, 15),
        gender="MALE",
    )

    allergy = Allergy.objects.create(
        patient=patient,
        allergen="Peanuts",
        allergy_type="FOOD",
        reaction="Skin rash",
        recorded_by=doctor,
    )

    assert allergy.severity == "UNKNOWN"
    assert allergy.status == "ACTIVE"


@pytest.mark.django_db
def test_doctor_cannot_be_deleted_if_allergy_exists():
    doctor_user = User.objects.create_user(
        email="doctor@example.com",
        password="testpassword123",
        first_name="Anil",
        last_name="Kumar",
    )

    doctor = Doctor.objects.create(
        user=doctor_user,
        medical_registration_number="MED123458",
        gender="MALE",
    )

    patient_user = User.objects.create_user(
        email="patient@example.com",
        password="testpassword123",
        first_name="Rahul",
        last_name="Menon",
    )

    patient = Patient.objects.create(
        user=patient_user,
        date_of_birth=date(1995, 5, 15),
        gender="MALE",
    )

    Allergy.objects.create(
        patient=patient,
        allergen="Penicillin",
        allergy_type="DRUG",
        reaction="Anaphylaxis",
        severity="LIFE_THREATENING",
        recorded_by=doctor,
    )

    with pytest.raises(ProtectedError):
        doctor.delete()


@pytest.mark.django_db
def test_patient_cannot_be_deleted_if_allergy_exists():
    doctor_user = User.objects.create_user(
        email="doctor@example.com",
        password="testpassword123",
        first_name="Anil",
        last_name="Kumar",
    )

    doctor = Doctor.objects.create(
        user=doctor_user,
        medical_registration_number="MED123459",
        gender="MALE",
    )

    patient_user = User.objects.create_user(
        email="patient@example.com",
        password="testpassword123",
        first_name="Rahul",
        last_name="Menon",
    )

    patient = Patient.objects.create(
        user=patient_user,
        date_of_birth=date(1995, 5, 15),
        gender="MALE",
    )

    Allergy.objects.create(
        patient=patient,
        allergen="Peanuts",
        allergy_type="FOOD",
        reaction="Difficulty breathing",
        severity="SEVERE",
        recorded_by=doctor,
    )

    with pytest.raises(ProtectedError):
        patient.delete()