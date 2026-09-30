import pytest
from rest_framework.test import APIClient


@pytest.fixture
def api_client():
    return APIClient()


@pytest.mark.django_db
def test_register_patient(api_client):
    data = {
        "email": "patient@example.com",
        "first_name": "John",
        "last_name": "Doe",
        "phone_number": "9876543210",
        "password": "securepass123",
        "password_confirm": "securepass123",
    }

    response = api_client.post(
        "/api/auth/register/",
        data,
        format="json",
    )

    assert response.status_code == 201

    assert response.data["email"] == "patient@example.com"
    assert response.data["first_name"] == "John"
    assert response.data["last_name"] == "Doe"
    assert response.data["phone_number"] == "9876543210"
    assert response.data["role"] == "PATIENT"

    assert "password" not in response.data
    assert "password_confirm" not in response.data


@pytest.mark.django_db
def test_register_rejects_password_mismatch(api_client):
    data = {
        "email": "patient@example.com",
        "first_name": "John",
        "last_name": "Doe",
        "password": "securepass123",
        "password_confirm": "differentpass123",
    }

    response = api_client.post(
        "/api/auth/register/",
        data,
        format="json",
    )

    assert response.status_code == 400
    assert "password_confirm" in response.data


@pytest.mark.django_db
def test_register_rejects_duplicate_email(api_client):
    first_data = {
        "email": "patient@example.com",
        "first_name": "John",
        "last_name": "Doe",
        "password": "securepass123",
        "password_confirm": "securepass123",
    }

    first_response = api_client.post(
        "/api/auth/register/",
        first_data,
        format="json",
    )

    assert first_response.status_code == 201

    second_data = {
        "email": "patient@example.com",
        "first_name": "Jane",
        "last_name": "Doe",
        "password": "securepass123",
        "password_confirm": "securepass123",
    }

    second_response = api_client.post(
        "/api/auth/register/",
        second_data,
        format="json",
    )

    assert second_response.status_code == 400
    assert "email" in second_response.data


@pytest.mark.django_db
def test_register_cannot_create_doctor(api_client):
    data = {
        "email": "doctor@example.com",
        "first_name": "John",
        "last_name": "Doctor",
        "password": "securepass123",
        "password_confirm": "securepass123",
        "role": "DOCTOR",
    }

    response = api_client.post(
        "/api/auth/register/",
        data,
        format="json",
    )

    assert response.status_code == 201
    assert response.data["role"] == "PATIENT"