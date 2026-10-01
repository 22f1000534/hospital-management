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


@pytest.mark.django_db
def test_refresh_token_returns_new_access_token(api_client, user):
    refresh_token = RefreshToken.for_user(user)

    response = api_client.post(
        "/api/auth/token/refresh/",
        {"refresh": str(refresh_token)},
        format="json",
    )

    assert response.status_code == 200
    assert "access" in response.data
    assert response.data["access"]


@pytest.mark.django_db
def test_refresh_token_rejects_invalid_token(api_client):
    response = api_client.post(
        "/api/auth/token/refresh/",
        {"refresh": "invalid-refresh-token"},
        format="json",
    )

    assert response.status_code == 401


@pytest.mark.django_db
def test_refresh_token_requires_refresh_token(api_client):
    response = api_client.post(
        "/api/auth/token/refresh/",
        {},
        format="json",
    )

    assert response.status_code == 400
    assert "refresh" in response.data