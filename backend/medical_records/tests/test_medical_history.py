import pytest
from datetime import date

from accounts.models import User
from doctors.models import Doctor
from medical_records.models import MedicalHistory
from patients.models import Patient
from django.db.models.deletion import ProtectedError

@pytest.mark.django_db
def test_create_medical_history():
    user = User.objects.create_user(
        email="doctor@example.com",
        password="testpassword123",
        first_name="Anil",
        last_name="Kumar",
    )

    doctor = Doctor.objects.create(
        user=user,
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
        date_of_birth="1995-05-15",
        gender="MALE",
    )

    history = MedicalHistory.objects.create(
        patient=patient,
        condition="Appendectomy",
        history_type="SURGERY",
        diagnosed_on=date(2018, 6, 12),
        status="RESOLVED",
        notes="Previous abdominal surgery.",
        recorded_by=doctor,
    )

    assert history.patient == patient
    assert history.recorded_by == doctor
    assert history.condition == "Appendectomy"
    assert history.history_type == "SURGERY"
    assert history.status == "RESOLVED"
    assert history.diagnosed_on == date(2018, 6, 12)


@pytest.mark.django_db
def test_medical_history_defaults_to_active():
    user = User.objects.create_user(
        email="doctor@example.com",
        password="testpassword123",
        first_name="Anil",
        last_name="Kumar",
    )

    doctor = Doctor.objects.create(
        user=user,
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

    history = MedicalHistory.objects.create(
        patient=patient,
        condition="Asthma",
        history_type="CHRONIC_CONDITION",
        recorded_by=doctor,
    )

    assert history.status == "ACTIVE"


@pytest.mark.django_db
def test_doctor_cannot_be_deleted_if_medical_history_exists():
    user = User.objects.create_user(
        email="doctor@example.com",
        password="testpassword123",
        first_name="Anil",
        last_name="Kumar",
    )

    doctor = Doctor.objects.create(
        user=user,
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

    MedicalHistory.objects.create(
        patient=patient,
        condition="Asthma",
        history_type="CHRONIC_CONDITION",
        recorded_by=doctor,
    )

    with pytest.raises(ProtectedError):
        doctor.delete()