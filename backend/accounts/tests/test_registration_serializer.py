import pytest

from accounts.models import User
from accounts.serializers import RegistrationSerializer
from patients.models import Patient


@pytest.mark.django_db
def test_registration_creates_user_and_patient():
    data = {
        "email": "patient@example.com",
        "first_name": "John",
        "last_name": "Doe",
        "phone_number": "9876543210",
        "password": "securepass123",
        "password_confirm": "securepass123",
    }

    serializer = RegistrationSerializer(data=data)

    assert serializer.is_valid(), serializer.errors

    user = serializer.save()

    assert User.objects.count() == 1
    assert Patient.objects.count() == 1

    assert user.email == "patient@example.com"
    assert user.role == "PATIENT"
    assert user.check_password("securepass123")

    assert hasattr(user, "patient_profile")
    assert user.patient_profile.user == user


@pytest.mark.django_db
def test_registration_rejects_password_mismatch():
    data = {
        "email": "patient@example.com",
        "first_name": "John",
        "last_name": "Doe",
        "password": "securepass123",
        "password_confirm": "differentpass123",
    }

    serializer = RegistrationSerializer(data=data)

    assert not serializer.is_valid()
    assert "password_confirm" in serializer.errors


@pytest.mark.django_db
def test_registration_rejects_duplicate_email():
    User.objects.create_user(
        email="patient@example.com",
        password="existingpass123",
        first_name="Existing",
        last_name="Patient",
    )

    data = {
        "email": "patient@example.com",
        "first_name": "John",
        "last_name": "Doe",
        "password": "securepass123",
        "password_confirm": "securepass123",
    }

    serializer = RegistrationSerializer(data=data)

    assert not serializer.is_valid()
    assert "email" in serializer.errors


@pytest.mark.django_db
def test_registration_does_not_allow_role_selection():
    data = {
        "email": "doctor@example.com",
        "first_name": "John",
        "last_name": "Doctor",
        "password": "securepass123",
        "password_confirm": "securepass123",
        "role": "DOCTOR",
    }

    serializer = RegistrationSerializer(data=data)

    assert serializer.is_valid(), serializer.errors

    user = serializer.save()

    assert user.role == "PATIENT"