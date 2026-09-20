import pytest
from django.db import IntegrityError
from django.db.models import ProtectedError

from accounts.models import User
from doctors.models import Doctor, DoctorOrganization
from master.models import Department
from organizations.models import Organization


@pytest.mark.django_db
def test_create_doctor_organization():
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

    organization = Organization.objects.create(
        created_by=user,
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
        joined_on="2025-01-01",
    )

    assert doctor_organization.doctor == doctor
    assert doctor_organization.organization == organization
    assert doctor_organization.department == department


@pytest.mark.django_db
def test_duplicate_doctor_organization_department_not_allowed():
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

    organization = Organization.objects.create(
        created_by=user,
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

    DoctorOrganization.objects.create(
        doctor=doctor,
        organization=organization,
        department=department,
        consultation_fee=800,
        joined_on="2025-01-01",
    )

    with pytest.raises(IntegrityError):
        DoctorOrganization.objects.create(
            doctor=doctor,
            organization=organization,
            department=department,
            consultation_fee=900,
            joined_on="2025-02-01",
        )

@pytest.mark.django_db
def test_doctor_can_belong_to_multiple_departments():
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

    organization = Organization.objects.create(
        created_by=user,
        name="City Hospital",
        organization_type="HOSPITAL",
        phone_number="9876543210",
        email="hospital@example.com",
        address_line_1="123 Hospital Road",
        city="Kozhikode",
        state="Kerala",
        postal_code="673001",
    )

    cardiology = Department.objects.create(name="Cardiology")
    neurology = Department.objects.create(name="Neurology")

    DoctorOrganization.objects.create(
        doctor=doctor,
        organization=organization,
        department=cardiology,
        joined_on="2025-01-01",
    )

    DoctorOrganization.objects.create(
        doctor=doctor,
        organization=organization,
        department=neurology,
        joined_on="2025-01-01",
    )

    assert doctor.organization_assignments.count() == 2

@pytest.mark.django_db
def test_doctor_can_belong_to_multiple_organizations():
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

    hospital_one = Organization.objects.create(
        created_by=user,
        name="City Hospital",
        organization_type="HOSPITAL",
        phone_number="9876543210",
        email="city@example.com",
        address_line_1="123 Hospital Road",
        city="Kozhikode",
        state="Kerala",
        postal_code="673001",
    )

    hospital_two = Organization.objects.create(
        created_by=user,
        name="Metro Hospital",
        organization_type="HOSPITAL",
        phone_number="9876543211",
        email="metro@example.com",
        address_line_1="456 Hospital Road",
        city="Kozhikode",
        state="Kerala",
        postal_code="673001",
    )

    department = Department.objects.create(name="Cardiology")

    DoctorOrganization.objects.create(
        doctor=doctor,
        organization=hospital_one,
        department=department,
        joined_on="2025-01-01",
    )

    DoctorOrganization.objects.create(
        doctor=doctor,
        organization=hospital_two,
        department=department,
        joined_on="2025-01-01",
    )

    assert doctor.organization_assignments.count() == 2

@pytest.mark.django_db
def test_deleting_doctor_deletes_assignment():
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

    organization = Organization.objects.create(
        created_by=user,
        name="City Hospital",
        organization_type="HOSPITAL",
        phone_number="9876543210",
        email="hospital@example.com",
        address_line_1="123 Hospital Road",
        city="Kozhikode",
        state="Kerala",
        postal_code="673001",
    )

    department = Department.objects.create(name="Cardiology")

    assignment = DoctorOrganization.objects.create(
        doctor=doctor,
        organization=organization,
        department=department,
        joined_on="2025-01-01",
    )

    assignment_id = assignment.id

    doctor.delete()

    assert not DoctorOrganization.objects.filter(id=assignment_id).exists()

@pytest.mark.django_db
def test_deleting_organization_deletes_assignment():
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

    organization = Organization.objects.create(
        created_by=user,
        name="City Hospital",
        organization_type="HOSPITAL",
        phone_number="9876543210",
        email="hospital@example.com",
        address_line_1="123 Hospital Road",
        city="Kozhikode",
        state="Kerala",
        postal_code="673001",
    )

    department = Department.objects.create(name="Cardiology")

    assignment = DoctorOrganization.objects.create(
        doctor=doctor,
        organization=organization,
        department=department,
        joined_on="2025-01-01",
    )

    assignment_id = assignment.id

    organization.delete()

    assert not DoctorOrganization.objects.filter(id=assignment_id).exists()

@pytest.mark.django_db
def test_deleting_department_with_assignment_is_protected():
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

    organization = Organization.objects.create(
        created_by=user,
        name="City Hospital",
        organization_type="HOSPITAL",
        phone_number="9876543210",
        email="hospital@example.com",
        address_line_1="123 Hospital Road",
        city="Kozhikode",
        state="Kerala",
        postal_code="673001",
    )

    department = Department.objects.create(name="Cardiology")

    DoctorOrganization.objects.create(
        doctor=doctor,
        organization=organization,
        department=department,
        joined_on="2025-01-01",
    )

    with pytest.raises(ProtectedError):
        department.delete()