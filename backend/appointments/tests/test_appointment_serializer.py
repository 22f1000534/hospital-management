from datetime import date, time

import pytest

from accounts.models import User
from appointments.choices import AppointmentStatus
from appointments.models import Appointment
from appointments.serializers import AppointmentCreateSerializer, AppointmentSerializer
from doctors.models import Doctor, DoctorOrganization
from master.models import Department
from organizations.models import Organization
from patients.models import Patient


@pytest.fixture
def appointment_data(db):
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

    organization = Organization.objects.create(
        created_by=doctor_user,
        name="City Hospital",
        organization_type="HOSPITAL",
        phone_number="9876543210",
        email="hospital@example.com",
        address_line_1="123 Hospital Road",
        city="Kozhikode",
        state="Kerala",
        postal_code="673001",
    )

    department = Department.objects.create(
        name="Cardiology",
    )

    doctor_organization = DoctorOrganization.objects.create(
        doctor=doctor,
        organization=organization,
        department=department,
        consultation_fee=800,
        joined_on=date(2025, 1, 1),
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

    appointment = Appointment.objects.create(
        patient=patient,
        doctor_organization=doctor_organization,
        appointment_date=date(2026, 10, 5),
        start_time=time(10, 30),
        end_time=time(10, 45),
        reason="Recurring headaches",
    )

    return {
        "appointment": appointment,
        "patient": patient,
        "doctor_organization": doctor_organization,
    }


@pytest.mark.django_db
def test_appointment_serializer_returns_expected_fields(appointment_data):
    appointment = appointment_data["appointment"]

    serializer = AppointmentSerializer(appointment)

    assert set(serializer.data.keys()) == {
        "id",
        "patient",
        "doctor_organization",
        "appointment_date",
        "start_time",
        "end_time",
        "status",
        "reason",
        "notes",
        "cancellation_reason",
        "created_at",
        "updated_at",
    }


@pytest.mark.django_db
def test_patient_and_status_are_read_only():
    serializer = AppointmentSerializer()

    assert serializer.fields["patient"].read_only is True
    assert serializer.fields["status"].read_only is True


@pytest.mark.django_db
def test_timestamps_are_read_only():
    serializer = AppointmentSerializer()

    assert serializer.fields["created_at"].read_only is True
    assert serializer.fields["updated_at"].read_only is True


@pytest.mark.django_db
def test_valid_booking_data_is_accepted(appointment_data):
    data = {
        "doctor_organization": str(
            appointment_data["doctor_organization"].id
        ),
        "appointment_date": "2026-10-10",
        "start_time": "11:00:00",
        "end_time": "11:15:00",
        "reason": "Headache",
    }

    serializer = AppointmentSerializer(data=data)

    assert serializer.is_valid(), serializer.errors


@pytest.mark.django_db
def test_doctor_organization_is_required():
    data = {
        "appointment_date": "2026-10-10",
        "start_time": "11:00:00",
        "end_time": "11:15:00",
        "reason": "Headache",
    }

    serializer = AppointmentSerializer(data=data)

    assert not serializer.is_valid()
    assert "doctor_organization" in serializer.errors


@pytest.mark.django_db
def test_appointment_date_is_required(appointment_data):
    data = {
        "doctor_organization": str(
            appointment_data["doctor_organization"].id
        ),
        "start_time": "11:00:00",
        "end_time": "11:15:00",
        "reason": "Headache",
    }

    serializer = AppointmentSerializer(data=data)

    assert not serializer.is_valid()
    assert "appointment_date" in serializer.errors


@pytest.mark.django_db
def test_client_cannot_set_patient_or_status(appointment_data):
    data = {
        "patient": str(appointment_data["patient"].id),
        "doctor_organization": str(
            appointment_data["doctor_organization"].id
        ),
        "appointment_date": "2026-10-10",
        "start_time": "11:00:00",
        "end_time": "11:15:00",
        "reason": "Headache",
        "status": "COMPLETED",
    }

    serializer = AppointmentSerializer(data=data)

    assert serializer.is_valid(), serializer.errors

    validated_data = serializer.validated_data

    assert "patient" not in validated_data
    assert "status" not in validated_data


@pytest.mark.django_db
def test_valid_appointment_booking(appointment_setup):
    data = {
    "doctor_organization": appointment_setup["appointment"].doctor_organization.id,
    "appointment_date": date(2026, 10, 6),
    "start_time": time(10, 30),
    "end_time": time(10, 45),
    "reason": "Fever and headache",
    }

    serializer = AppointmentCreateSerializer(data=data)

    assert serializer.is_valid(), serializer.errors

@pytest.mark.django_db
def test_end_time_must_be_after_start_time(appointment_setup):
    data = {
    "doctor_organization": appointment_setup["appointment"].doctor_organization.id,
    "appointment_date": date(2026, 10, 6),
    "start_time": time(10, 45),
    "end_time": time(10, 30),
    "reason": "Fever",
    }

    serializer = AppointmentCreateSerializer(data=data)

    assert not serializer.is_valid()
    assert "end_time" in serializer.errors

@pytest.mark.django_db
def test_inactive_doctor_organization_cannot_be_booked(appointment_setup):
    doctor_organization = appointment_setup[
    "appointment"
    ].doctor_organization

    doctor_organization.is_active = False
    doctor_organization.save()

    data = {
        "doctor_organization": doctor_organization.id,
        "appointment_date": date(2026, 10, 6),
        "start_time": time(10, 30),
        "end_time": time(10, 45),
        "reason": "Fever",
    }

    serializer = AppointmentCreateSerializer(data=data)

    assert not serializer.is_valid()
    assert "doctor_organization" in serializer.errors

@pytest.mark.django_db
def test_overlapping_appointment_is_rejected(appointment_setup):
    appointment = appointment_setup["appointment"]

    data = {
        "doctor_organization": appointment.doctor_organization.id,
        "appointment_date": appointment.appointment_date,
        "start_time": time(10, 15),
        "end_time": time(10, 45),
        "reason": "Fever",
    }

    serializer = AppointmentCreateSerializer(data=data)

    assert not serializer.is_valid()
    assert "non_field_errors" in serializer.errors

@pytest.mark.django_db
def test_adjacent_appointment_is_allowed(appointment_setup):
    appointment = appointment_setup["appointment"]

    data = {
        "doctor_organization": appointment.doctor_organization.id,
        "appointment_date": appointment.appointment_date,
        "start_time": appointment.end_time,
        "end_time": time(11, 0),
        "reason": "Follow-up",
    }

    serializer = AppointmentCreateSerializer(data=data)

    assert serializer.is_valid(), serializer.errors

@pytest.mark.django_db
def test_patient_status_and_server_fields_are_read_only(appointment_setup):
    data = {
    "patient": appointment_setup["other_patient_user"].id,
    "doctor_organization": appointment_setup["appointment"].doctor_organization.id,
    "appointment_date": date(2026, 10, 6),
    "start_time": time(10, 30),
    "end_time": time(10, 45),
    "status": AppointmentStatus.CANCELLED,
    "notes": "Malicious client input",
    "cancellation_reason": "Malicious cancellation",
    "reason": "Fever",
    }

    serializer = AppointmentCreateSerializer(data=data)

    assert serializer.is_valid(), serializer.errors

    assert "patient" not in serializer.validated_data
    assert "status" not in serializer.validated_data
    assert "notes" not in serializer.validated_data
    assert "cancellation_reason" not in serializer.validated_data