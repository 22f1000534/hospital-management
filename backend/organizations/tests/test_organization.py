import pytest
from django.contrib.auth import get_user_model

from organizations.choices import OrganizationType
from organizations.models import Organization

User = get_user_model()


@pytest.fixture
def user(db):
    return User.objects.create_user(
        email="admin@example.com",
        password="testpass123",
        first_name="Test",
        last_name="Admin",
    )


@pytest.fixture
def organization(user):
    return Organization.objects.create(
        created_by=user,
        name="City Hospital",
        organization_type=OrganizationType.HOSPITAL,
        phone_number="9876543210",
        email="hospital@example.com",
        address_line_1="123 Hospital Road",
        city="Kozhikode",
        state="Kerala",
        postal_code="673001",
    )


@pytest.mark.django_db
def test_create_organization(user):
    organization = Organization.objects.create(
        created_by=user,
        name="City Hospital",
        organization_type=OrganizationType.HOSPITAL,
        phone_number="9876543210",
        email="hospital@example.com",
        address_line_1="123 Hospital Road",
        city="Kozhikode",
        state="Kerala",
        postal_code="673001",
    )

    assert organization.name == "City Hospital"
    assert organization.created_by == user
    assert organization.organization_type == OrganizationType.HOSPITAL
    assert organization.country == "India"
    assert organization.is_verified is False
    assert organization.is_active is True


@pytest.mark.django_db
def test_slug_is_generated_from_name(user):
    organization = Organization.objects.create(
        created_by=user,
        name="City General Hospital",
        organization_type=OrganizationType.HOSPITAL,
        phone_number="9876543210",
        email="hospital@example.com",
        address_line_1="123 Hospital Road",
        city="Kozhikode",
        state="Kerala",
        postal_code="673001",
    )

    assert organization.slug == "city-general-hospital"


@pytest.mark.django_db
def test_existing_slug_is_preserved(user):
    organization = Organization.objects.create(
        created_by=user,
        name="City Hospital",
        slug="city-hospital-kozhikode",
        organization_type=OrganizationType.HOSPITAL,
        phone_number="9876543210",
        email="hospital@example.com",
        address_line_1="123 Hospital Road",
        city="Kozhikode",
        state="Kerala",
        postal_code="673001",
    )

    assert organization.slug == "city-hospital-kozhikode"


@pytest.mark.django_db
def test_optional_fields_can_be_blank(user):
    organization = Organization.objects.create(
        created_by=user,
        name="City Hospital",
        organization_type=OrganizationType.HOSPITAL,
        phone_number="9876543210",
        email="hospital@example.com",
        address_line_1="123 Hospital Road",
        city="Kozhikode",
        state="Kerala",
        postal_code="673001",
    )

    assert organization.description == ""
    assert organization.website == ""
    assert organization.address_line_2 == ""
    assert not organization.logo


@pytest.mark.django_db
def test_organization_string_representation(organization):
    assert str(organization) == "City Hospital"

