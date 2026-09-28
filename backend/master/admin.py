from django.contrib import admin

from master.models import (
    Department,
    Language,
    Qualification,
    Specialization,
)


@admin.register(Qualification)
class QualificationAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "is_active")
    search_fields = ("code", "name")
    list_filter = ("is_active",)


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ("name", "is_active")
    search_fields = ("name",)
    list_filter = ("is_active",)


@admin.register(Specialization)
class SpecializationAdmin(admin.ModelAdmin):
    list_display = ("name", "department", "is_active")
    search_fields = ("name",)
    list_filter = ("department", "is_active")


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ("code", "name")
    search_fields = ("code", "name")
