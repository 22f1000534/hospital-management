from django.contrib import admin

from organizations.models import Organization


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "organization_type",
        "city",
        "state",
        "is_verified",
        "is_active",
        "created_at",
    )

    list_filter = (
        "organization_type",
        "is_verified",
        "is_active",
        "city",
        "state",
    )

    search_fields = (
        "name",
        "city",
        "email",
        "phone_number",
    )

    readonly_fields = (
        "id",
        "slug",
        "created_at",
        "updated_at",
    )

    ordering = ("name",)

    prepopulated_fields = {}
