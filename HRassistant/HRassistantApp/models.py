from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):

    ROLE_CHOICES = (
        ("HR", "HR"),
        ("EMPLOYEE", "Employee"),
    )

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile"
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default="EMPLOYEE"
    )

    employee_id = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        unique=True
    )

    department = models.CharField(
        max_length=100,
        blank=True
    )

    designation = models.CharField(
        max_length=100,
        blank=True
    )

    def __str__(self):
        return f"{self.user.username} - {self.role}"


class SecurityAuditLog(models.Model):
    event_type = models.CharField(max_length=100)
    message = models.TextField()
    risk_level = models.CharField(max_length=20, default="Low")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.event_type} - {self.risk_level}"