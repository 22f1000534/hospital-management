import pytest
from rest_framework.test import APIRequestFactory

from appointments.permissions import CanAccessAppointment
from organizations.models import OrganizationMembership


def get_request(user):
    request = APIRequestFactory().get("/api/appointments/")
    request.user = user
    return request


@pytest.mark.django_db
def test_patient_can_access_own_appointment(appointment_setup):
    request = get_request(appointment_setup["patient_user"])

    permission = CanAccessAppointment()

    assert permission.has_object_permission(
        request,
        None,
        appointment_setup["appointment"],
    )


@pytest.mark.django_db
def test_patient_cannot_access_other_patient_appointment(appointment_setup):
    request = get_request(appointment_setup["patient_user"])

    permission = CanAccessAppointment()

    assert not permission.has_object_permission(
        request,
        None,
        appointment_setup["other_appointment"],
    )


@pytest.mark.django_db
def test_doctor_can_access_assigned_appointment(appointment_setup):
    request = get_request(appointment_setup["doctor_user"])

    permission = CanAccessAppointment()

    assert permission.has_object_permission(
        request,
        None,
        appointment_setup["appointment"],
    )


@pytest.mark.django_db
def test_doctor_cannot_access_other_doctors_appointment(appointment_setup):
    request = get_request(appointment_setup["doctor_user"])

    permission = CanAccessAppointment()

    assert not permission.has_object_permission(
        request,
        None,
        appointment_setup["other_appointment"],
    )


@pytest.mark.django_db
def test_organization_admin_can_access_organization_appointment(
    appointment_setup,
):
    request = get_request(appointment_setup["org_admin"])

    permission = CanAccessAppointment()

    assert permission.has_object_permission(
        request,
        None,
        appointment_setup["appointment"],
    )


@pytest.mark.django_db
def test_organization_admin_cannot_access_other_organization_appointment(
    appointment_setup,
):
    request = get_request(appointment_setup["org_admin"])

    permission = CanAccessAppointment()

    assert not permission.has_object_permission(
        request,
        None,
        appointment_setup["other_appointment"],
    )


@pytest.mark.django_db
def test_super_admin_can_access_any_appointment(appointment_setup):
    request = get_request(appointment_setup["super_admin"])

    permission = CanAccessAppointment()

    assert permission.has_object_permission(
        request,
        None,
        appointment_setup["appointment"],
    )

    assert permission.has_object_permission(
        request,
        None,
        appointment_setup["other_appointment"],
    )


@pytest.mark.django_db
def test_inactive_organization_membership_denies_access(
    appointment_setup,
):
    membership = OrganizationMembership.objects.get(
        organization=appointment_setup["organization"],
        user=appointment_setup["org_admin"],
    )
    membership.is_active = False
    membership.save()

    request = get_request(appointment_setup["org_admin"])

    permission = CanAccessAppointment()

    assert not permission.has_object_permission(
        request,
        None,
        appointment_setup["appointment"],
    )