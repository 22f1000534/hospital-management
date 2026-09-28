from datetime import date, time

import pytest
from django.db.models import ProtectedError

from accounts.models import User
from appointments.models import Appointment
from consultations.models import Consultation
from doctors.models import Doctor, DoctorOrganization
from master.models import Department
from organizations.models import Organization
from patients.models import Patient
from treatments.models import Diagnosis, Treatment


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
def test_create_treatment(diagnosis_data):
    from treatments.models import Treatment

    treatment = Treatment.objects.create(
        consultation=diagnosis_data["consultation"],
        treatment_type="PHYSIOTHERAPY",
        description="Physiotherapy for lower back pain.",
        start_date=date(2026, 10, 5),
        instructions="Attend physiotherapy twice a week.",
    )

    assert treatment.consultation == diagnosis_data["consultation"]
    assert treatment.treatment_type == "PHYSIOTHERAPY"
    assert treatment.description == "Physiotherapy for lower back pain."
    assert treatment.status == "PLANNED"


@pytest.mark.django_db
def test_treatment_can_be_linked_to_multiple_diagnoses(diagnosis_data):
    consultation = diagnosis_data["consultation"]

    diagnosis_1 = Diagnosis.objects.create(
        consultation=consultation,
        condition="Type 2 Diabetes",
        diagnosis_type="PRIMARY",
    )

    diagnosis_2 = Diagnosis.objects.create(
        consultation=consultation,
        condition="Hypertension",
        diagnosis_type="SECONDARY",
    )

    treatment = Treatment.objects.create(
        consultation=consultation,
        treatment_type="LIFESTYLE",
        description="Dietary and exercise modification.",
    )

    treatment.diagnoses.add(diagnosis_1, diagnosis_2)

    assert treatment.diagnoses.count() == 2
    assert diagnosis_1 in treatment.diagnoses.all()
    assert diagnosis_2 in treatment.diagnoses.all()


@pytest.mark.django_db
def test_diagnosis_can_have_multiple_treatments(diagnosis_data):
    consultation = diagnosis_data["consultation"]

    diagnosis = Diagnosis.objects.create(
        consultation=consultation,
        condition="Type 2 Diabetes",
        diagnosis_type="PRIMARY",
    )

    treatment_1 = Treatment.objects.create(
        consultation=consultation,
        treatment_type="MEDICATION",
        description="Medication for diabetes.",
    )

    treatment_2 = Treatment.objects.create(
        consultation=consultation,
        treatment_type="DIET",
        description="Dietary modification.",
    )

    diagnosis.treatments.add(treatment_1, treatment_2)

    assert diagnosis.treatments.count() == 2
    assert treatment_1 in diagnosis.treatments.all()
    assert treatment_2 in diagnosis.treatments.all()


@pytest.mark.django_db
def test_consultation_deletion_is_protected_by_treatment(diagnosis_data):
    consultation = diagnosis_data["consultation"]

    Treatment.objects.create(
        consultation=consultation,
        treatment_type="PHYSIOTHERAPY",
        description="Physiotherapy treatment.",
    )

    with pytest.raises(ProtectedError):
        consultation.delete()


@pytest.mark.django_db
def test_treatment_str(diagnosis_data):
    treatment = Treatment.objects.create(
        consultation=diagnosis_data["consultation"],
        treatment_type="PHYSIOTHERAPY",
        description="Physiotherapy treatment.",
    )

    assert str(treatment) == f"PHYSIOTHERAPY - {treatment.consultation}"
