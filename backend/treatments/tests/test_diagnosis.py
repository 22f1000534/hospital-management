from datetime import date, time

import pytest
from django.db import IntegrityError
from django.db.models import ProtectedError

from accounts.models import User
from appointments.models import Appointment
from consultations.models import Consultation
from doctors.models import Doctor, DoctorOrganization
from master.models import Department
from organizations.models import Organization
from patients.models import Patient
from treatments.models import Diagnosis


@pytest.fixture
def diagnosis_data():
    doctor_user = User.objects.create_user(
        email="doctor@example.com",
        password="testpass123",
        first_name="John",
        last_name="Doctor",
    )

    doctor = Doctor.objects.create(
        user=doctor_user,
        medical_registration_number="MED12345",
        gender="MALE",
        practice_started_on=date(2015, 1, 1),
    )

    organization_owner = User.objects.create_user(
        email="owner@example.com",
        password="testpass123",
        first_name="Hospital",
        last_name="Admin",
    )

    organization = Organization.objects.create(
        created_by=organization_owner,
        name="City Hospital",
        organization_type="HOSPITAL",
        phone_number="9876543210",
        email="hospital@example.com",
        address_line_1="Main Road",
        city="Kozhikode",
        state="Kerala",
        country="India",
        postal_code="673001",
    )

    department = Department.objects.create(
        name="Cardiology",
    )

    doctor_organization = DoctorOrganization.objects.create(
        doctor=doctor,
        organization=organization,
        department=department,
        consultation_fee=500,
        joined_on=date(2020, 1, 1),
    )

    patient_user = User.objects.create_user(
        email="patient@example.com",
        password="testpass123",
        first_name="Jane",
        last_name="Patient",
    )

    patient = Patient.objects.create(
        user=patient_user,
        date_of_birth=date(1995, 5, 10),
        gender="FEMALE",
    )

    appointment = Appointment.objects.create(
        patient=patient,
        doctor_organization=doctor_organization,
        appointment_date=date(2026, 10, 1),
        start_time=time(10, 0),
        end_time=time(10, 30),
        reason="Routine consultation",
    )

    consultation = Consultation.objects.create(
        appointment=appointment,
        chief_complaint="Chest pain",
    )

    return {
        "doctor": doctor,
        "organization": organization,
        "department": department,
        "doctor_organization": doctor_organization,
        "patient": patient,
        "appointment": appointment,
        "consultation": consultation,
    }


@pytest.mark.django_db
def test_create_diagnosis(diagnosis_data):
    diagnosis = Diagnosis.objects.create(
        consultation=diagnosis_data["consultation"],
        condition="Hypertension",
        diagnosis_type="PRIMARY",
        notes="Blood pressure consistently elevated.",
    )

    assert diagnosis.consultation == diagnosis_data["consultation"]
    assert diagnosis.condition == "Hypertension"
    assert diagnosis.diagnosis_type == "PRIMARY"
    assert diagnosis.diagnosed_on == date.today()


@pytest.mark.django_db
def test_consultation_can_have_multiple_diagnoses(diagnosis_data):
    consultation = diagnosis_data["consultation"]

    primary = Diagnosis.objects.create(
        consultation=consultation,
        condition="Hypertension",
        diagnosis_type="PRIMARY",
    )

    secondary = Diagnosis.objects.create(
        consultation=consultation,
        condition="Type 2 Diabetes",
        diagnosis_type="SECONDARY",
    )

    provisional = Diagnosis.objects.create(
        consultation=consultation,
        condition="Possible thyroid disorder",
        diagnosis_type="PROVISIONAL",
    )

    assert consultation.diagnoses.count() == 3
    assert primary in consultation.diagnoses.all()
    assert secondary in consultation.diagnoses.all()
    assert provisional in consultation.diagnoses.all()


@pytest.mark.django_db
def test_consultation_can_have_only_one_primary_diagnosis(diagnosis_data):
    consultation = diagnosis_data["consultation"]

    Diagnosis.objects.create(
        consultation=consultation,
        condition="Hypertension",
        diagnosis_type="PRIMARY",
    )

    with pytest.raises(IntegrityError):
        Diagnosis.objects.create(
            consultation=consultation,
            condition="Type 2 Diabetes",
            diagnosis_type="PRIMARY",
        )


@pytest.mark.django_db
def test_multiple_secondary_and_provisional_diagnoses_are_allowed(diagnosis_data):
    consultation = diagnosis_data["consultation"]

    Diagnosis.objects.create(
        consultation=consultation,
        condition="Hypertension",
        diagnosis_type="PRIMARY",
    )

    Diagnosis.objects.create(
        consultation=consultation,
        condition="Type 2 Diabetes",
        diagnosis_type="SECONDARY",
    )

    Diagnosis.objects.create(
        consultation=consultation,
        condition="Vitamin D deficiency",
        diagnosis_type="SECONDARY",
    )

    Diagnosis.objects.create(
        consultation=consultation,
        condition="Possible thyroid disorder",
        diagnosis_type="PROVISIONAL",
    )

    Diagnosis.objects.create(
        consultation=consultation,
        condition="Possible anemia",
        diagnosis_type="PROVISIONAL",
    )

    assert consultation.diagnoses.count() == 5


@pytest.mark.django_db
def test_consultation_deletion_is_protected(diagnosis_data):
    consultation = diagnosis_data["consultation"]

    Diagnosis.objects.create(
        consultation=consultation,
        condition="Hypertension",
        diagnosis_type="PRIMARY",
    )

    with pytest.raises(ProtectedError):
        consultation.delete()


@pytest.mark.django_db
def test_diagnosis_str(diagnosis_data):
    diagnosis = Diagnosis.objects.create(
        consultation=diagnosis_data["consultation"],
        condition="Hypertension",
        diagnosis_type="PRIMARY",
    )

    assert str(diagnosis) == f"Hypertension - {diagnosis.consultation}"