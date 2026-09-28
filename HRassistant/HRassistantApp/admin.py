from django.contrib import admin
from .models import (
    SecurityAuditLog,
    UserProfile,
    HRDocument,
    HRDocumentChunk,
)


@admin.register(SecurityAuditLog)
class SecurityAuditLogAdmin(admin.ModelAdmin):
    list_display = (
        "event_type",
        "risk_level",
        "created_at",
    )

    list_filter = (
        "risk_level",
        "event_type",
    )

    search_fields = (
        "message",
    )


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "role",
        "employee_id",
        "department",
        "designation",
    )

    list_filter = (
        "role",
        "department",
    )

    search_fields = (
        "user__username",
        "user__email",
        "employee_id",
        "department",
    )


@admin.register(HRDocument)
class HRDocumentAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "uploaded_by",
        "uploaded_at",
    )

    search_fields = (
        "title",
    )

    list_filter = (
        "uploaded_at",
    )


@admin.register(HRDocumentChunk)
class HRDocumentChunkAdmin(admin.ModelAdmin):
    list_display = (
        "document",
        "id",
    )

    search_fields = (
        "content",
        "document__title",
    )