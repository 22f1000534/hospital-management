from datetime import date, time

import pytest

from accounts.choices import UserRole
from accounts.models import User
from appointments.models import Appointment
from doctors.models import Doctor, DoctorOrganization
from master.models import Department
from organizations.models import Organization, OrganizationMembership
from patients.models import Patient


@pytest.fixture
def appointment_setup(db):
    doctor_user = User.objects.create_user(
        email="doctor@example.com",
        password="testpassword123",
        first_name="Anil",
        last_name="Kumar",
        role=UserRole.DOCTOR,
    )

    other_doctor_user = User.objects.create_user(
        email="otherdoctor@example.com",
        password="testpassword123",
        first_name="Other",
        last_name="Doctor",
        role=UserRole.DOCTOR,
    )

    patient_user = User.objects.create_user(
        email="patient@example.com",
        password="testpassword123",
        first_name="Rahul",
        last_name="Menon",
        role=UserRole.PATIENT,
    )

    other_patient_user = User.objects.create_user(
        email="otherpatient@example.com",
        password="testpassword123",
        first_name="Other",
        last_name="Patient",
        role=UserRole.PATIENT,
    )

    org_admin = User.objects.create_user(
        email="admin@example.com",
        password="testpassword123",
        first_name="Organization",
        last_name="Admin",
        role=UserRole.ORG_ADMIN,
    )

    other_org_admin = User.objects.create_user(
        email="otheradmin@example.com",
        password="testpassword123",
        first_name="Other",
        last_name="Admin",
        role=UserRole.ORG_ADMIN,
    )

    super_admin = User.objects.create_user(
        email="superadmin@example.com",
        password="testpassword123",
        first_name="Super",
        last_name="Admin",
        role=UserRole.SUPER_ADMIN,
    )

    doctor = Doctor.objects.create(
        user=doctor_user,
        medical_registration_number="MED123456",
        gender="MALE",
    )

    other_doctor = Doctor.objects.create(
        user=other_doctor_user,
        medical_registration_number="MED123457",
        gender="MALE",
    )

    organization = Organization.objects.create(
        created_by=org_admin,
        name="City Hospital",
        organization_type="HOSPITAL",
        phone_number="9876543210",
        email="hospital@example.com",
        address_line_1="123 Hospital Road",
        city="Kozhikode",
        state="Kerala",
        postal_code="673001",
    )

    other_organization = Organization.objects.create(
        created_by=other_org_admin,
        name="Metro Clinic",
        organization_type="CLINIC",
        phone_number="9876543211",
        email="clinic@example.com",
        address_line_1="456 Clinic Road",
        city="Kozhikode",
        state="Kerala",
        postal_code="673002",
    )

    OrganizationMembership.objects.create(
        organization=organization,
        user=org_admin,
    )

    other_organization_membership = OrganizationMembership.objects.create(
        organization=other_organization,
        user=other_org_admin,
    )

    department = Department.objects.create(
        name="Cardiology",
    )

    other_department = Department.objects.create(
        name="Neurology",
    )

    doctor_organization = DoctorOrganization.objects.create(
        doctor=doctor,
        organization=organization,
        department=department,
        consultation_fee=800,
        joined_on=date(2025, 1, 1),
    )

    other_doctor_organization = DoctorOrganization.objects.create(
        doctor=other_doctor,
        organization=other_organization,
        department=other_department,
        consultation_fee=900,
        joined_on=date(2025, 1, 1),
    )

    patient = Patient.objects.create(
        user=patient_user,
        date_of_birth=date(1995, 5, 15),
        gender="MALE",
    )

    other_patient = Patient.objects.create(
        user=other_patient_user,
        date_of_birth=date(1996, 6, 20),
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

    other_appointment = Appointment.objects.create(
        patient=other_patient,
        doctor_organization=other_doctor_organization,
        appointment_date=date(2026, 10, 5),
        start_time=time(11, 00),
        end_time=time(11, 15),
        reason="Back pain",
    )

    return {
        "appointment": appointment,
        "other_appointment": other_appointment,
        "doctor_user": doctor_user,
        "other_doctor_user": other_doctor_user,
        "patient_user": patient_user,
        "other_patient_user": other_patient_user,
        "org_admin": org_admin,
        "other_org_admin": other_org_admin,
        "super_admin": super_admin,
        "organization": organization,
        "other_organization": other_organization,
        "other_organization_membership": other_organization_membership,
    }