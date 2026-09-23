import pytest
from datetime import date
from django.db import IntegrityError

from accounts.models import User
from patients.models import Patient


@pytest.mark.django_db
def test_create_patient():
    user = User.objects.create_user(
        email="patient@example.com",
        password="testpassword123",
        first_name="Rahul",
        last_name="Menon",
    )

    patient = Patient.objects.create(
        user=user,
        date_of_birth=date(1995, 5, 15),
        gender="MALE",
        blood_group="O+",
        address_line_1="123 Main Road",
        city="Kozhikode",
        state="Kerala",
        postal_code="673001",
    )

    assert patient.user == user
    assert patient.date_of_birth == date(1995, 5, 15)
    assert patient.gender == "MALE"
    assert patient.blood_group == "O+"


@pytest.mark.django_db
def test_create_patient_with_minimal_information():
    user = User.objects.create_user(
        email="patient@example.com",
        password="testpassword123",
    )

    patient = Patient.objects.create(
        user=user,
    )

    assert patient.user == user
    assert patient.date_of_birth is None
    assert patient.gender == ""
    assert patient.blood_group == ""
    assert patient.address_line_1 == ""
    assert patient.address_line_2 == ""
    assert patient.city == ""
    assert patient.state == ""
    assert patient.postal_code == ""
    assert patient.country == "India"


@pytest.mark.django_db
def test_user_cannot_have_multiple_patient_profiles():
    user = User.objects.create_user(
        email="patient@example.com",
        password="testpassword123",
    )

    Patient.objects.create(user=user)

    with pytest.raises(IntegrityError):
        Patient.objects.create(user=user)