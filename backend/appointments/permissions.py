from rest_framework.permissions import BasePermission

from accounts.choices import UserRole


class CanAccessAppointment(BasePermission):
    """
    Allows access to an appointment based on the user's role
    and relationship to the appointment.
    """

    def has_object_permission(self, request, view, obj):
        user = request.user

        if not user.is_authenticated:
            return False

        if user.role == UserRole.SUPER_ADMIN:
            return True

        if user.role == UserRole.PATIENT:
            return obj.patient.user == user

        if user.role == UserRole.DOCTOR:
            return obj.doctor_organization.doctor.user == user

        if user.role == UserRole.ORG_ADMIN:
            return obj.doctor_organization.organization.memberships.filter(
                user=user,
                is_active=True,
            ).exists()

        return False