import pytest
from django.contrib.auth.models import AnonymousUser
from rest_framework.test import APIRequestFactory

from accounts.models import User
from accounts.permissions.roles import (
    IsDoctor,
    IsOrganizationAdmin,
    IsPatient,
    IsSuperAdmin,
)


@pytest.fixture
def request_factory():
    return APIRequestFactory()


@pytest.fixture
def patient():
    return User.objects.create_user(
        email="patient@example.com",
        password="securepass123",
        first_name="John",
        last_name="Patient",
        role="PATIENT",
    )


@pytest.fixture
def doctor():
    return User.objects.create_user(
        email="doctor@example.com",
        password="securepass123",
        first_name="Jane",
        last_name="Doctor",
        role="DOCTOR",
    )


@pytest.fixture
def organization_admin():
    return User.objects.create_user(
        email="admin@example.com",
        password="securepass123",
        first_name="Organization",
        last_name="Admin",
        role="ORG_ADMIN",
    )


@pytest.fixture
def super_admin():
    return User.objects.create_user(
        email="superadmin@example.com",
        password="securepass123",
        first_name="Super",
        last_name="Admin",
        role="SUPER_ADMIN",
    )


@pytest.mark.django_db
def test_is_patient_allows_patient(request_factory, patient):
    request = request_factory.get("/")
    request.user = patient

    permission = IsPatient()

    assert permission.has_permission(request, None) is True


@pytest.mark.django_db
def test_is_patient_rejects_doctor(request_factory, doctor):
    request = request_factory.get("/")
    request.user = doctor

    permission = IsPatient()

    assert permission.has_permission(request, None) is False


@pytest.mark.django_db
def test_is_doctor_allows_doctor(request_factory, doctor):
    request = request_factory.get("/")
    request.user = doctor

    permission = IsDoctor()

    assert permission.has_permission(request, None) is True


@pytest.mark.django_db
def test_is_doctor_rejects_patient(request_factory, patient):
    request = request_factory.get("/")
    request.user = patient

    permission = IsDoctor()

    assert permission.has_permission(request, None) is False


@pytest.mark.django_db
def test_is_organization_admin_allows_organization_admin(
    request_factory,
    organization_admin,
):
    request = request_factory.get("/")
    request.user = organization_admin

    permission = IsOrganizationAdmin()

    assert permission.has_permission(request, None) is True


@pytest.mark.django_db
def test_is_organization_admin_rejects_patient(
    request_factory,
    patient,
):
    request = request_factory.get("/")
    request.user = patient

    permission = IsOrganizationAdmin()

    assert permission.has_permission(request, None) is False


@pytest.mark.django_db
def test_is_super_admin_allows_super_admin(request_factory, super_admin):
    request = request_factory.get("/")
    request.user = super_admin

    permission = IsSuperAdmin()

    assert permission.has_permission(request, None) is True


@pytest.mark.django_db
def test_is_super_admin_rejects_patient(request_factory, patient):
    request = request_factory.get("/")
    request.user = patient

    permission = IsSuperAdmin()

    assert permission.has_permission(request, None) is False


@pytest.mark.django_db
def test_is_patient_rejects_unauthenticated_user(request_factory):
    request = request_factory.get("/")
    request.user = AnonymousUser()

    permission = IsPatient()

    assert permission.has_permission(request, None) is False


@pytest.mark.django_db
def test_is_doctor_rejects_unauthenticated_user(request_factory):
    request = request_factory.get("/")
    request.user = AnonymousUser()

    permission = IsDoctor()

    assert permission.has_permission(request, None) is False


@pytest.mark.django_db
def test_is_organization_admin_rejects_unauthenticated_user(
    request_factory,
):
    request = request_factory.get("/")
    request.user = AnonymousUser()

    permission = IsOrganizationAdmin()

    assert permission.has_permission(request, None) is False


@pytest.mark.django_db
def test_is_super_admin_rejects_unauthenticated_user(request_factory):
    request = request_factory.get("/")
    request.user = AnonymousUser()

    permission = IsSuperAdmin()

    assert permission.has_permission(request, None) is False