from django.contrib import admin
from .models import SecurityAuditLog, UserProfile


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