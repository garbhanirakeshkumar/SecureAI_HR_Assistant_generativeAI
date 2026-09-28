from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from HRassistantApp.views import (
    home,
    security_scanner,
    hr_chatbot,
    security_dashboard,
    user_login,
    user_logout,
    high_risk_logs,
    medium_risk_logs,
    low_risk_logs,
    all_security_logs,
    hr_dashboard,
    employee_dashboard,
    employee_list,
    add_employee,
    profile,
    hr_documents,
    delete_hr_document,
)


urlpatterns = [

    # Admin
    path("admin/", admin.site.urls),

    # Home
    path("", home, name="home"),

    # Authentication
    path("login/", user_login, name="user_login"),
    path("logout/", user_logout, name="user_logout"),

    # Dashboards
    path(
        "hr-dashboard/",
        hr_dashboard,
        name="hr_dashboard"
    ),

    path(
        "employee-dashboard/",
        employee_dashboard,
        name="employee_dashboard"
    ),

    # Profile
    path(
        "profile/",
        profile,
        name="profile"
    ),

    # Employee Management
    path(
        "employees/",
        employee_list,
        name="employee_list"
    ),

    path(
        "employees/add/",
        add_employee,
        name="add_employee"
    ),

    # AI HR Assistant
    path(
        "hr-chatbot/",
        hr_chatbot,
        name="hr_chatbot"
    ),

    # Security
    path(
        "security-scanner/",
        security_scanner,
        name="security_scanner"
    ),

    path(
        "security-dashboard/",
        security_dashboard,
        name="security_dashboard"
    ),

    # Security Logs
    path(
        "all-security-logs/",
        all_security_logs,
        name="all_security_logs"
    ),

    path(
        "high-risk-logs/",
        high_risk_logs,
        name="high_risk_logs"
    ),

    path(
        "medium-risk-logs/",
        medium_risk_logs,
        name="medium_risk_logs"
    ),

    path(
        "low-risk-logs/",
        low_risk_logs,
        name="low_risk_logs"
    ),
    path(
    "hr/documents/",
    hr_documents,
    name="hr_documents"
),
path(
    "hr/documents/delete/<int:document_id>/",
    delete_hr_document,
    name="delete_hr_document"
),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )