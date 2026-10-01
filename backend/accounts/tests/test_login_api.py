import pytest
from rest_framework.test import APIClient

from accounts.models import User


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user():
    return User.objects.create_user(
        email="patient@example.com",
        password="securepass123",
        first_name="John",
        last_name="Doe",
    )


@pytest.mark.django_db
def test_login_returns_tokens_and_user(api_client, user):
    response = api_client.post(
        "/api/auth/login/",
        {
            "email": "patient@example.com",
            "password": "securepass123",
        },
        format="json",
    )

    assert response.status_code == 200

    assert "access" in response.data
    assert "refresh" in response.data
    assert "user" in response.data

    assert response.data["user"]["email"] == "patient@example.com"
    assert response.data["user"]["first_name"] == "John"
    assert response.data["user"]["last_name"] == "Doe"

    assert "password" not in response.data
    assert "password" not in response.data["user"]


@pytest.mark.django_db
def test_login_rejects_wrong_password(api_client):
    response = api_client.post(
        "/api/auth/login/",
        {
            "email": "patient@example.com",
            "password": "wrongpassword",
        },
        format="json",
    )

    assert response.status_code == 403


@pytest.mark.django_db
def test_login_rejects_unknown_email(api_client):
    response = api_client.post(
        "/api/auth/login/",
        {
            "email": "unknown@example.com",
            "password": "securepass123",
        },
        format="json",
    )
    assert response.status_code == 403