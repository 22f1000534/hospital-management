from django.contrib import admin

from doctors.models import Doctor


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