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
from treatments.models import Treatment, Prescription


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
def test_create_prescription(diagnosis_data):
    treatment = Treatment.objects.create(
        consultation=diagnosis_data["consultation"],
        treatment_type="MEDICATION",
        description="Medication for diabetes.",
    )

    prescription = Prescription.objects.create(
        treatment=treatment,
        medication_name="Metformin",
        dosage="500 mg",
        frequency="Twice daily",
        route="Oral",
        start_date=date(2026, 10, 1),
        end_date=date(2026, 10, 31),
        instructions="Take after food.",
    )

    assert prescription.treatment == treatment
    assert prescription.medication_name == "Metformin"
    assert prescription.dosage == "500 mg"
    assert prescription.frequency == "Twice daily"
    assert prescription.start_date == date(2026, 10, 1)
    assert prescription.end_date == date(2026, 10, 31)
    assert prescription.status == "ACTIVE"


@pytest.mark.django_db
def test_treatment_can_have_multiple_prescriptions(diagnosis_data):
    treatment = Treatment.objects.create(
        consultation=diagnosis_data["consultation"],
        treatment_type="MEDICATION",
        description="Medication treatment.",
    )

    prescription_1 = Prescription.objects.create(
        treatment=treatment,
        medication_name="Metformin",
        dosage="500 mg",
        frequency="Twice daily",
        start_date=date(2026, 10, 1),
    )

    prescription_2 = Prescription.objects.create(
        treatment=treatment,
        medication_name="Vitamin D",
        dosage="60,000 IU",
        frequency="Once weekly",
        start_date=date(2026, 10, 1),
    )

    assert treatment.prescriptions.count() == 2
    assert prescription_1 in treatment.prescriptions.all()
    assert prescription_2 in treatment.prescriptions.all()


@pytest.mark.django_db
def test_prescription_can_have_no_end_date(diagnosis_data):
    treatment = Treatment.objects.create(
        consultation=diagnosis_data["consultation"],
        treatment_type="MEDICATION",
        description="Long-term medication.",
    )

    prescription = Prescription.objects.create(
        treatment=treatment,
        medication_name="Metformin",
        dosage="500 mg",
        frequency="Once daily",
        start_date=date(2026, 10, 1),
    )

    assert prescription.end_date is None


@pytest.mark.django_db
def test_treatment_deletion_is_protected(diagnosis_data):
    treatment = Treatment.objects.create(
        consultation=diagnosis_data["consultation"],
        treatment_type="MEDICATION",
        description="Medication treatment.",
    )

    Prescription.objects.create(
        treatment=treatment,
        medication_name="Metformin",
        dosage="500 mg",
        frequency="Twice daily",
        start_date=date(2026, 10, 1),
    )

    with pytest.raises(ProtectedError):
        treatment.delete()


@pytest.mark.django_db
def test_prescription_str(diagnosis_data):
    treatment = Treatment.objects.create(
        consultation=diagnosis_data["consultation"],
        treatment_type="MEDICATION",
        description="Medication treatment.",
    )

    prescription = Prescription.objects.create(
        treatment=treatment,
        medication_name="Metformin",
        dosage="500 mg",
        frequency="Twice daily",
        start_date=date(2026, 10, 1),
    )

    assert str(prescription) == f"Metformin - {treatment}"