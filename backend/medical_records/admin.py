from django.contrib import admin

# Register your models here.
from medical_records.models import MedicalHistory


@admin.register(MedicalHistory)
class MedicalHistoryAdmin(admin.ModelAdmin):
    list_display = (
        "patient",
        "condition",
        "history_type",
        "status",
        "diagnosed_on",
        "recorded_by",
    )

    search_fields = (
        "patient__user__first_name",
        "patient__user__last_name",
        "patient__user__email",
        "condition",
        "notes",
    )

    list_filter = (
        "history_type",
        "status",
    )

    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
    )
