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

class HRDocument(models.Model):
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to="hr_documents/")
    uploaded_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="uploaded_hr_documents"
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class HRDocumentChunk(models.Model):
    document = models.ForeignKey(
        HRDocument,
        on_delete=models.CASCADE,
        related_name="chunks"
    )
    content = models.TextField()
    embedding = models.JSONField()

    def __str__(self):
        return f"{self.document.title} - Chunk {self.id}"