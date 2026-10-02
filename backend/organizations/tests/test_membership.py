import pytest
from django.contrib.auth import get_user_model
from django.db import IntegrityError

from organizations.models import Organization, OrganizationMembership

User = get_user_model()


@pytest.fixture
def organization(db):
    user = User.objects.create_user(
        email="creator@example.com",
        password="testpass123",
        first_name="Organization",
        last_name="Creator",
    )

    return Organization.objects.create(
        created_by=user,
        name="City Hospital",
        organization_type="HOSPITAL",
        phone_number="9876543210",
        email="hospital@example.com",
        address_line_1="123 Hospital Road",
        city="Kozhikode",
        state="Kerala",
        postal_code="673001",
    )


@pytest.fixture
def organization_2(db):
    user = User.objects.create_user(
        email="creator2@example.com",
        password="testpass123",
        first_name="Organization",
        last_name="Creator",
    )

    return Organization.objects.create(
        created_by=user,
        name="Metro Clinic",
        organization_type="CLINIC",
        phone_number="9876543211",
        email="clinic@example.com",
        address_line_1="456 Clinic Road",
        city="Kozhikode",
        state="Kerala",
        postal_code="673002",
    )


@pytest.fixture
def org_admin(db):
    return User.objects.create_user(
        email="admin@example.com",
        password="testpass123",
        first_name="Organization",
        last_name="Admin",
        role="ORG_ADMIN",
    )


@pytest.fixture
def org_admin_2(db):
    return User.objects.create_user(
        email="admin2@example.com",
        password="testpass123",
        first_name="Second",
        last_name="Admin",
        role="ORG_ADMIN",
    )


@pytest.mark.django_db
def test_user_can_be_admin_of_multiple_organizations(
    organization,
    organization_2,
    org_admin,
):
    membership_1 = OrganizationMembership.objects.create(
        organization=organization,
        user=org_admin,
    )
    membership_2 = OrganizationMembership.objects.create(
        organization=organization_2,
        user=org_admin,
    )

    assert membership_1.is_active is True
    assert membership_2.is_active is True
    assert org_admin.organization_memberships.count() == 2


@pytest.mark.django_db
def test_organization_can_have_multiple_admins(
    organization,
    org_admin,
    org_admin_2,
):
    OrganizationMembership.objects.create(
        organization=organization,
        user=org_admin,
    )
    OrganizationMembership.objects.create(
        organization=organization,
        user=org_admin_2,
    )

    assert organization.memberships.count() == 2


@pytest.mark.django_db
def test_duplicate_active_membership_is_not_allowed(
    organization,
    org_admin,
):
    OrganizationMembership.objects.create(
        organization=organization,
        user=org_admin,
    )

    with pytest.raises(IntegrityError):
        OrganizationMembership.objects.create(
            organization=organization,
            user=org_admin,
        )


@pytest.mark.django_db
def test_inactive_membership_can_be_recreated(
    organization,
    org_admin,
):
    old_membership = OrganizationMembership.objects.create(
        organization=organization,
        user=org_admin,
        is_active=False,
    )

    new_membership = OrganizationMembership.objects.create(
        organization=organization,
        user=org_admin,
    )

    assert old_membership.is_active is False
    assert new_membership.is_active is True
    assert organization.memberships.count() == 2


@pytest.mark.django_db
def test_inactive_membership_does_not_count_as_active(
    organization,
    org_admin,
):
    membership = OrganizationMembership.objects.create(
        organization=organization,
        user=org_admin,
        is_active=False,
    )

    assert membership.is_active is False
    assert organization.memberships.filter(is_active=True).count() == 0
    assert (
        org_admin.organization_memberships.filter(is_active=True).count()
        == 0
    )


@pytest.mark.django_db
def test_deleting_organization_deletes_memberships(
    organization,
    org_admin,
):
    OrganizationMembership.objects.create(
        organization=organization,
        user=org_admin,
    )

    organization.delete()

    assert OrganizationMembership.objects.filter(
        user=org_admin,
    ).count() == 0