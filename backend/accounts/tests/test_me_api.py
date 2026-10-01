import pytest
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

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


@pytest.fixture
def access_token(user):
    refresh_token = RefreshToken.for_user(user)

    return str(refresh_token.access_token)


@pytest.mark.django_db
def test_me_returns_authenticated_user(api_client, user, access_token):
    api_client.credentials(
        HTTP_AUTHORIZATION=f"Bearer {access_token}",
    )

    response = api_client.get("/api/auth/me/")

    assert response.status_code == 200

    assert response.data["id"] == str(user.id)
    assert response.data["email"] == "patient@example.com"
    assert response.data["first_name"] == "John"
    assert response.data["last_name"] == "Doe"
    assert response.data["role"] == "PATIENT"


@pytest.mark.django_db
def test_me_requires_authentication(api_client):
    response = api_client.get("/api/auth/me/")

    assert response.status_code == 401


@pytest.mark.django_db
def test_me_rejects_invalid_access_token(api_client):
    api_client.credentials(
        HTTP_AUTHORIZATION="Bearer invalid-token",
    )

    response = api_client.get("/api/auth/me/")

    assert response.status_code == 401


@pytest.mark.django_db
def test_me_rejects_refresh_token(api_client, user):
    refresh_token = RefreshToken.for_user(user)

    api_client.credentials(
        HTTP_AUTHORIZATION=f"Bearer {str(refresh_token)}",
    )

    response = api_client.get("/api/auth/me/")

    assert response.status_code == 401