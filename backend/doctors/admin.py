from django.contrib import admin

from doctors.models import Doctor, DoctorOrganization


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "medical_registration_number",
        "is_verified",
        "is_active",
    )

    search_fields = (
        "user__first_name",
        "user__last_name",
        "user__email",
        "medical_registration_number",
    )

    list_filter = (
        "gender",
        "is_verified",
        "is_active",
    )

    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
    )

@admin.register(DoctorOrganization)
class DoctorOrganizationAdmin(admin.ModelAdmin):
    list_display = (
        "doctor",
        "organization",
        "department",
        "consultation_fee",
        "joined_on",
        "left_on",
        "is_active",
    )

    list_filter = (
        "organization",
        "department",
        "is_active",
    )

    search_fields = (
        "doctor__user__first_name",
        "doctor__user__last_name",
        "organization__name",
        "department__name",
    )