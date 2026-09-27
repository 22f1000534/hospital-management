from datetime import date, time

import pytest
from django.db.models.deletion import ProtectedError

from accounts.models import User
from appointments.models import Appointment
from doctors.models import Doctor, DoctorOrganization
from master.models import Department
from organizations.models import Organization
from patients.models import Patient


@pytest.mark.django_db
def test_create_appointment():
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

    assert appointment.patient == patient
    assert appointment.doctor_organization == doctor_organization
    assert appointment.doctor_organization.doctor == doctor
    assert appointment.doctor_organization.organization == organization
    assert appointment.doctor_organization.department == department
    assert appointment.status == "PENDING"


@pytest.mark.django_db
def test_patient_cannot_be_deleted_if_appointment_exists():
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

    with pytest.raises(ProtectedError):
        patient.delete()


@pytest.mark.django_db
def test_doctor_organization_cannot_be_deleted_if_appointment_exists():
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

    Appointment.objects.create(
        patient=patient,
        doctor_organization=doctor_organization,
        appointment_date=date(2026, 10, 5),
        start_time=time(10, 30),
        end_time=time(10, 45),
    )

    with pytest.raises(ProtectedError):
        doctor_organization.delete()