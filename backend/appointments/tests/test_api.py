from datetime import timedelta

import pytest
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient

from appointments.choices import AppointmentStatus


@pytest.fixture
def api_client():
    return APIClient()


@pytest.mark.django_db
def test_unauthenticated_user_cannot_list_appointments(api_client):
    response = api_client.get("/api/appointments/")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_patient_can_list_own_appointments(api_client, appointment_setup):
    api_client.force_authenticate(user=appointment_setup["patient_user"])

    response = api_client.get("/api/appointments/")

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]["id"] == str(
        appointment_setup["appointment"].id
    )


@pytest.mark.django_db
def test_doctor_can_list_assigned_appointments(api_client, appointment_setup):
    api_client.force_authenticate(user=appointment_setup["doctor_user"])

    response = api_client.get("/api/appointments/")

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]["id"] == str(
        appointment_setup["appointment"].id
    )


@pytest.mark.django_db
def test_organization_admin_can_list_organization_appointments(
    api_client,
    appointment_setup,
):
    api_client.force_authenticate(user=appointment_setup["org_admin"])

    response = api_client.get("/api/appointments/")

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]["id"] == str(
        appointment_setup["appointment"].id
    )


@pytest.mark.django_db
def test_super_admin_can_list_all_appointments(api_client, appointment_setup):
    api_client.force_authenticate(user=appointment_setup["super_admin"])

    response = api_client.get("/api/appointments/")

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 2

    appointment_ids = {
        result["id"] for result in response.data
    }

    assert str(appointment_setup["appointment"].id) in appointment_ids
    assert str(appointment_setup["other_appointment"].id) in appointment_ids


@pytest.mark.django_db
def test_unauthenticated_user_cannot_retrieve_appointment(
    api_client,
    appointment_setup,
):
    appointment_id = appointment_setup["appointment"].id

    response = api_client.get(
        f"/api/appointments/{appointment_id}/"
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_patient_can_retrieve_own_appointment(
    api_client,
    appointment_setup,
):
    api_client.force_authenticate(user=appointment_setup["patient_user"])

    appointment_id = appointment_setup["appointment"].id

    response = api_client.get(
        f"/api/appointments/{appointment_id}/"
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.data["id"] == str(appointment_id)


@pytest.mark.django_db
def test_patient_cannot_retrieve_other_patient_appointment(
    api_client,
    appointment_setup,
):
    api_client.force_authenticate(user=appointment_setup["patient_user"])

    appointment_id = appointment_setup["other_appointment"].id

    response = api_client.get(
        f"/api/appointments/{appointment_id}/"
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_doctor_can_retrieve_assigned_appointment(
    api_client,
    appointment_setup,
):
    api_client.force_authenticate(user=appointment_setup["doctor_user"])

    appointment_id = appointment_setup["appointment"].id

    response = api_client.get(
        f"/api/appointments/{appointment_id}/"
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.data["id"] == str(appointment_id)


@pytest.mark.django_db
def test_doctor_cannot_retrieve_other_doctors_appointment(
    api_client,
    appointment_setup,
):
    api_client.force_authenticate(user=appointment_setup["doctor_user"])

    appointment_id = appointment_setup["other_appointment"].id

    response = api_client.get(
        f"/api/appointments/{appointment_id}/"
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_organization_admin_can_retrieve_organization_appointment(
    api_client,
    appointment_setup,
):
    api_client.force_authenticate(user=appointment_setup["org_admin"])

    appointment_id = appointment_setup["appointment"].id

    response = api_client.get(
        f"/api/appointments/{appointment_id}/"
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.data["id"] == str(appointment_id)


@pytest.mark.django_db
def test_organization_admin_cannot_retrieve_other_organization_appointment(
    api_client,
    appointment_setup,
):
    api_client.force_authenticate(user=appointment_setup["org_admin"])

    appointment_id = appointment_setup["other_appointment"].id

    response = api_client.get(
        f"/api/appointments/{appointment_id}/"
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_super_admin_can_retrieve_any_appointment(
    api_client,
    appointment_setup,
):
    api_client.force_authenticate(user=appointment_setup["super_admin"])

    appointment_id = appointment_setup["other_appointment"].id

    response = api_client.get(
        f"/api/appointments/{appointment_id}/"
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.data["id"] == str(appointment_id)


@pytest.mark.django_db
def test_nonexistent_appointment_returns_404(
    api_client,
    appointment_setup,
):
    api_client.force_authenticate(user=appointment_setup["super_admin"])

    response = api_client.get(
        "/api/appointments/00000000-0000-0000-0000-000000000000/"
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND

#post request to /api/appointments/

@pytest.mark.django_db
def test_patient_can_book_appointment(api_client, appointment_setup):
    api_client.force_authenticate(user=appointment_setup["patient_user"])

    data = {
        "doctor_organization": str(
            appointment_setup["appointment"].doctor_organization.id
        ),
        "appointment_date": "2026-10-06",
        "start_time": "10:30:00",
        "end_time": "10:45:00",
        "reason": "Fever and headache",
    }

    response = api_client.post(
        "/api/appointments/",
        data,
        format="json",
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["reason"] == "Fever and headache"
    assert response.data["patient"] == appointment_setup["appointment"].patient.id
    assert response.data["status"] == "PENDING"


@pytest.mark.django_db
def test_unauthenticated_user_cannot_book_appointment(
    api_client,
    appointment_setup,
):
    data = {
        "doctor_organization": str(
            appointment_setup["appointment"].doctor_organization.id
        ),
        "appointment_date": "2026-10-06",
        "start_time": "10:30:00",
        "end_time": "10:45:00",
        "reason": "Fever",
    }

    response = api_client.post(
        "/api/appointments/",
        data,
        format="json",
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_doctor_cannot_book_appointment(api_client, appointment_setup):
    api_client.force_authenticate(user=appointment_setup["doctor_user"])

    data = {
        "doctor_organization": str(
            appointment_setup["appointment"].doctor_organization.id
        ),
        "appointment_date": "2026-10-06",
        "start_time": "10:30:00",
        "end_time": "10:45:00",
        "reason": "Fever",
    }

    response = api_client.post(
        "/api/appointments/",
        data,
        format="json",
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_organization_admin_cannot_book_appointment(
    api_client,
    appointment_setup,
):
    api_client.force_authenticate(user=appointment_setup["org_admin"])

    data = {
        "doctor_organization": str(
            appointment_setup["appointment"].doctor_organization.id
        ),
        "appointment_date": "2026-10-06",
        "start_time": "10:30:00",
        "end_time": "10:45:00",
        "reason": "Fever",
    }

    response = api_client.post(
        "/api/appointments/",
        data,
        format="json",
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_super_admin_cannot_book_appointment(
    api_client,
    appointment_setup,
):
    api_client.force_authenticate(user=appointment_setup["super_admin"])

    data = {
        "doctor_organization": str(
            appointment_setup["appointment"].doctor_organization.id
        ),
        "appointment_date": "2026-10-06",
        "start_time": "10:30:00",
        "end_time": "10:45:00",
        "reason": "Fever",
    }

    response = api_client.post(
        "/api/appointments/",
        data,
        format="json",
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_patient_cannot_book_overlapping_appointment(
    api_client,
    appointment_setup,
):
    api_client.force_authenticate(user=appointment_setup["patient_user"])

    existing = appointment_setup["appointment"]

    data = {
        "doctor_organization": str(existing.doctor_organization.id),
        "appointment_date": str(existing.appointment_date),
        "start_time": "10:15:00",
        "end_time": "10:45:00",
        "reason": "Overlapping appointment",
    }

    response = api_client.post(
        "/api/appointments/",
        data,
        format="json",
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_patient_cannot_create_invalid_time_appointment(
    api_client,
    appointment_setup,
):
    api_client.force_authenticate(user=appointment_setup["patient_user"])

    data = {
        "doctor_organization": str(
            appointment_setup["appointment"].doctor_organization.id
        ),
        "appointment_date": "2026-10-06",
        "start_time": "11:00:00",
        "end_time": "10:30:00",
        "reason": "Invalid time",
    }

    response = api_client.post(
        "/api/appointments/",
        data,
        format="json",
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_patient_can_cancel_own_appointment(api_client, appointment_setup):
    appointment = appointment_setup["appointment"]

    appointment.appointment_date = timezone.localdate() + timedelta(days=1)
    appointment.save(update_fields=["appointment_date"])
    data = {
        "cancellation_reason": "Personal reason",
    }

    api_client.force_authenticate(
        user=appointment_setup["patient_user"]
    )

    response = api_client.post(
        f"/api/appointments/{appointment.id}/cancel/",
        data,
        format="json",
    )

    # assert response.status_code == 200
    assert response.status_code == 200, response.data
    assert response.data["status"] == AppointmentStatus.CANCELLED
    assert response.data["cancellation_reason"] == "Personal reason"

    appointment.refresh_from_db()

    assert appointment.status == AppointmentStatus.CANCELLED
    assert (
        appointment.cancellation_reason
        == "Personal reason"
    )

def test_unauthenticated_user_cannot_cancel_appointment(
    api_client,
    appointment_setup,
):
    response = api_client.post(
        f"/api/appointments/{appointment_setup['appointment'].id}/cancel/",
        {"cancellation_reason": "Personal reason"},
        format="json",
    )

    assert response.status_code == 401


def test_doctor_cannot_cancel_appointment(
    api_client,
    appointment_setup,
):
    api_client.force_authenticate(
        user=appointment_setup["doctor_user"]
    )

    response = api_client.post(
        f"/api/appointments/{appointment_setup['appointment'].id}/cancel/",
        {"cancellation_reason": "Personal reason"},
        format="json",
    )

    assert response.status_code == 403


def test_patient_cannot_cancel_another_patients_appointment(
    api_client,
    appointment_setup,
):
    api_client.force_authenticate(
        user=appointment_setup["other_patient_user"]
    )

    response = api_client.post(
        f"/api/appointments/{appointment_setup['appointment'].id}/cancel/",
        {"cancellation_reason": "Personal reason"},
        format="json",
    )

    assert response.status_code == 404


def test_patient_cannot_cancel_completed_appointment(
    api_client,
    appointment_setup,
):
    appointment = appointment_setup["appointment"]
    appointment.status = AppointmentStatus.COMPLETED
    appointment.save(update_fields=["status"])

    api_client.force_authenticate(
        user=appointment_setup["patient_user"]
    )

    response = api_client.post(
        f"/api/appointments/{appointment.id}/cancel/",
        {"cancellation_reason": "Personal reason"},
        format="json",
    )

    assert response.status_code == 400


def test_patient_cannot_cancel_no_show_appointment(
    api_client,
    appointment_setup,
):
    appointment = appointment_setup["appointment"]
    appointment.status = AppointmentStatus.NO_SHOW
    appointment.save(update_fields=["status"])

    api_client.force_authenticate(
        user=appointment_setup["patient_user"]
    )

    response = api_client.post(
        f"/api/appointments/{appointment.id}/cancel/",
        {"cancellation_reason": "Personal reason"},
        format="json",
    )

    assert response.status_code == 400


def test_patient_cannot_cancel_already_cancelled_appointment(
    api_client,
    appointment_setup,
):
    appointment = appointment_setup["appointment"]
    appointment.status = AppointmentStatus.CANCELLED
    appointment.save(update_fields=["status"])

    api_client.force_authenticate(
        user=appointment_setup["patient_user"]
    )

    response = api_client.post(
        f"/api/appointments/{appointment.id}/cancel/",
        {"cancellation_reason": "Personal reason"},
        format="json",
    )

    assert response.status_code == 400


def test_cancellation_requires_reason(
    api_client,
    appointment_setup,
):
    api_client.force_authenticate(
        user=appointment_setup["patient_user"]
    )

    response = api_client.post(
        f"/api/appointments/{appointment_setup['appointment'].id}/cancel/",
        {"cancellation_reason": "   "},
        format="json",
    )

    assert response.status_code == 400


def test_patient_cannot_cancel_after_appointment_started(
    api_client,
    appointment_setup,
):
    appointment = appointment_setup["appointment"]

    appointment.appointment_date = timezone.localdate()
    appointment.start_time = (
        timezone.localtime() - timedelta(hours=1)
    ).time()
    appointment.save(
        update_fields=[
            "appointment_date",
            "start_time",
        ]
    )

    api_client.force_authenticate(
        user=appointment_setup["patient_user"]
    )

    response = api_client.post(
        f"/api/appointments/{appointment.id}/cancel/",
        {"cancellation_reason": "Personal reason"},
        format="json",
    )

    assert response.status_code == 400
    assert (
        response.data["non_field_errors"][0]
        == "An appointment cannot be cancelled after it has started."
    )