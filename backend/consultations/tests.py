from datetime import date, time

import pytest
from django.db import IntegrityError
from django.db.models import ProtectedError

from accounts.models import User
from appointments.models import Appointment
from doctors.models import Doctor, DoctorOrganization
from master.models import Department
from organizations.models import Organization
from patients.models import Patient
from consultations.models import Consultation


@pytest.fixture
def consultation_data():
    user = User.objects.create_user(
        email="doctor@example.com",
        password="testpass123",
        first_name="John",
        last_name="Doe",
    )

    doctor = Doctor.objects.create(
        user=user,
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
        reason="Chest pain",
    )

    return {
        "doctor": doctor,
        "organization": organization,
        "department": department,
        "doctor_organization": doctor_organization,
        "patient": patient,
        "appointment": appointment,
    }


@pytest.mark.django_db
def test_create_consultation(consultation_data):
    consultation = Consultation.objects.create(
        appointment=consultation_data["appointment"],
        chief_complaint="Chest pain",
        history_of_present_illness="Pain started two days ago.",
        examination_notes="Blood pressure normal.",
        clinical_notes="Possible cardiac-related symptoms.",
        doctor_notes="Further investigation required.",
    )

    assert consultation.appointment == consultation_data["appointment"]
    assert consultation.chief_complaint == "Chest pain"
    assert consultation.status == "IN_PROGRESS"


@pytest.mark.django_db
def test_appointment_can_have_only_one_consultation(consultation_data):
    appointment = consultation_data["appointment"]

    Consultation.objects.create(
        appointment=appointment,
        chief_complaint="Headache",
    )

    with pytest.raises(IntegrityError):
        Consultation.objects.create(
            appointment=appointment,
            chief_complaint="Another complaint",
        )


@pytest.mark.django_db
def test_appointment_deletion_is_protected(consultation_data):
    appointment = consultation_data["appointment"]

    Consultation.objects.create(
        appointment=appointment,
        chief_complaint="Chest pain",
    )

    with pytest.raises(ProtectedError):
        appointment.delete()


@pytest.mark.django_db
def test_consultation_str(consultation_data):
    consultation = Consultation.objects.create(
        appointment=consultation_data["appointment"],
        chief_complaint="Chest pain",
    )

    assert str(consultation) == f"Consultation - {consultation.appointment}"