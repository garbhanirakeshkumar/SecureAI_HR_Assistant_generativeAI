from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .response_validator import validate_response


from .security_scanner import scan_prompt, mask_sensitive_data
from .document_processor import extract_text_from_file
from .document_ingestion import process_document
from .gemini_rag import generate_hr_answer
from .models import (
    SecurityAuditLog,
    UserProfile,
    HRDocument,
)


# =========================================================
# HOME
# =========================================================

@login_required(login_url="user_login")
def home(request):
    if request.user.profile.role == "HR":
        return redirect("hr_dashboard")
    else:
        return redirect("employee_dashboard")


# =========================================================
# LOGIN
# =========================================================

def user_login(request):
    error = None

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)

            if user.profile.role == "HR":
                return redirect("hr_dashboard")
            else:
                return redirect("employee_dashboard")

        else:
            error = "Invalid username or password."

    return render(
        request,
        "login.html",
        {
            "error": error
        }
    )


# =========================================================
# LOGOUT
# =========================================================

def user_logout(request):
    logout(request)
    return redirect("user_login")


# =========================================================
# HR DASHBOARD
# =========================================================

@login_required(login_url="user_login")
def hr_dashboard(request):

    if request.user.profile.role != "HR":
        return redirect("employee_dashboard")

    total_employees = UserProfile.objects.filter(
        role="EMPLOYEE"
    ).count()

    total_security_events = SecurityAuditLog.objects.count()

    high_risk_events = SecurityAuditLog.objects.filter(
        risk_level="High"
    ).count()

    return render(
        request,
        "hr_dashboard.html",
        {
            "total_employees": total_employees,
            "total_security_events": total_security_events,
            "high_risk_events": high_risk_events,
        }
    )


# =========================================================
# EMPLOYEE DASHBOARD
# =========================================================

@login_required(login_url="user_login")
def employee_dashboard(request):

    if request.user.profile.role != "EMPLOYEE":
        return redirect("hr_dashboard")

    return render(
        request,
        "employee_dashboard.html"
    )


# =========================================================
# PROFILE
# =========================================================

@login_required(login_url="user_login")
def profile(request):

    return render(
        request,
        "profile.html",
        {
            "profile": request.user.profile
        }
    )


# =========================================================
# SECURITY SCANNER
# HR ONLY
# =========================================================

@login_required(login_url="user_login")
def security_scanner(request):

    if request.user.profile.role != "HR":
        return redirect("employee_dashboard")

    result = None
    masked_message = None

    if request.method == "POST":

        message = request.POST.get(
            "message",
            ""
        ).strip()

        if message:

            result = scan_prompt(message)

            masked_message = mask_sensitive_data(
                message
            )

            SecurityAuditLog.objects.create(
                event_type=(
                    "Suspicious Request"
                    if result["is_suspicious"]
                    else "Security Scan"
                ),
                message=masked_message,
                risk_level=result["risk_level"]
            )

    return render(
        request,
        "security_scanner.html",
        {
            "result": result,
            "masked_message": masked_message,
        }
    )


# =========================================================
# HR CHATBOT
# AVAILABLE TO HR + EMPLOYEES
# =========================================================

@login_required(login_url="user_login")
def hr_chatbot(request):

    response = None
    validation = None
    scan_result = None

    if request.method == "POST":

        message = request.POST.get(
            "message",
            ""
        ).strip()

        # -------------------------------------------------
        # 1. Empty input validation
        # -------------------------------------------------

        if not message:

            response = (
                "Please enter an HR-related question."
            )

            validation = validate_response(
                response
            )

        else:

            # -------------------------------------------------
            # 2. Scan user input
            # -------------------------------------------------

            scan_result = scan_prompt(
                message
            )

            # -------------------------------------------------
            # 3. Block suspicious requests
            # -------------------------------------------------

            if scan_result["is_suspicious"]:

                masked_message = mask_sensitive_data(
                    message
                )

                SecurityAuditLog.objects.create(
                    event_type="Suspicious Request",
                    message=masked_message,
                    risk_level=scan_result["risk_level"]
                )

                response = (
                    "I can't process that request. "
                    "Please ask a valid HR-related question."
                )

                validation = validate_response(
                    response
                )

            else:

                # -------------------------------------------------
                # 4. Generate answer using Gemini + RAG
                # -------------------------------------------------

                try:

                    response = generate_hr_answer(
                        message
                    )

                except Exception:

                    response = (
                        "Sorry, I couldn't generate a "
                        "response right now. Please try "
                        "again later or contact HR."
                    )

                    SecurityAuditLog.objects.create(
                        event_type="AI Generation Error",
                        message=(
                            "Gemini response generation failed."
                        ),
                        risk_level="Medium"
                    )

                # -------------------------------------------------
                # 5. Validate AI response
                # -------------------------------------------------

                validation = validate_response(
                    response
                )

                # -------------------------------------------------
                # 6. Block unsafe AI response
                # -------------------------------------------------

                if not validation["is_safe"]:

                    masked_response = mask_sensitive_data(
                        response
                    )

                    SecurityAuditLog.objects.create(
                        event_type="Unsafe AI Response",
                        message=masked_response,
                        risk_level="Medium"
                    )

                    response = (
                        "The generated response could not "
                        "pass security validation. Please "
                        "contact HR for further assistance."
                    )

                    validation = validate_response(
                        response
                    )

    return render(
        request,
        "hr_chatbot.html",
        {
            "response": response,
            "validation": validation,
            "scan_result": scan_result,
        }
    )


# =========================================================
# SECURITY DASHBOARD
# HR ONLY
# =========================================================

@login_required(login_url="user_login")
def security_dashboard(request):

    if request.user.profile.role != "HR":
        return redirect("employee_dashboard")

    # Total security events

    total_events = SecurityAuditLog.objects.count()

    # High-risk events

    high_risk_events = SecurityAuditLog.objects.filter(
        risk_level="High"
    ).count()

    # Medium-risk events

    medium_risk_events = SecurityAuditLog.objects.filter(
        risk_level="Medium"
    ).count()

    # Low-risk events

    low_risk_events = SecurityAuditLog.objects.filter(
        risk_level="Low"
    ).count()

    # Latest 10 events

    recent_logs = SecurityAuditLog.objects.order_by(
        "-created_at"
    )[:10]

    return render(
        request,
        "security_dashboard.html",
        {
            "total_events": total_events,
            "high_risk_events": high_risk_events,
            "medium_risk_events": medium_risk_events,
            "low_risk_events": low_risk_events,
            "recent_logs": recent_logs,
        }
    )


# =========================================================
# ALL SECURITY LOGS
# HR ONLY
# =========================================================

@login_required(login_url="user_login")
def all_security_logs(request):

    if request.user.profile.role != "HR":
        return redirect("employee_dashboard")

    logs = SecurityAuditLog.objects.order_by(
        "-created_at"
    )

    return render(
        request,
        "all_security_logs.html",
        {
            "logs": logs
        }
    )


# =========================================================
# HIGH-RISK LOGS
# HR ONLY
# =========================================================

@login_required(login_url="user_login")
def high_risk_logs(request):

    if request.user.profile.role != "HR":
        return redirect("employee_dashboard")

    logs = SecurityAuditLog.objects.filter(
        risk_level="High"
    ).order_by(
        "-created_at"
    )

    return render(
        request,
        "high_risk_logs.html",
        {
            "logs": logs
        }
    )


# =========================================================
# MEDIUM-RISK LOGS
# HR ONLY
# =========================================================

@login_required(login_url="user_login")
def medium_risk_logs(request):

    if request.user.profile.role != "HR":
        return redirect("employee_dashboard")

    logs = SecurityAuditLog.objects.filter(
        risk_level="Medium"
    ).order_by(
        "-created_at"
    )

    return render(
        request,
        "medium_risk_logs.html",
        {
            "logs": logs
        }
    )


# =========================================================
# LOW-RISK LOGS
# HR ONLY
# =========================================================

@login_required(login_url="user_login")
def low_risk_logs(request):

    if request.user.profile.role != "HR":
        return redirect("employee_dashboard")

    logs = SecurityAuditLog.objects.filter(
        risk_level="Low"
    ).order_by(
        "-created_at"
    )

    return render(
        request,
        "low_risk_logs.html",
        {
            "logs": logs
        }
    )


# =========================================================
# EMPLOYEE LIST
# HR ONLY
# =========================================================

@login_required(login_url="user_login")
def employee_list(request):

    if request.user.profile.role != "HR":
        return redirect("employee_dashboard")

    employees = UserProfile.objects.filter(
        role="EMPLOYEE"
    ).select_related(
        "user"
    )

    return render(
        request,
        "employee_list.html",
        {
            "employees": employees
        }
    )


# =========================================================
# ADD EMPLOYEE
# HR ONLY
# =========================================================

@login_required(login_url="user_login")
def add_employee(request):

    if request.user.profile.role != "HR":
        return redirect("employee_dashboard")

    error = None

    if request.method == "POST":

        username = request.POST.get(
            "username",
            ""
        ).strip()

        email = request.POST.get(
            "email",
            ""
        ).strip()

        password = request.POST.get(
            "password",
            ""
        )

        employee_id = request.POST.get(
            "employee_id",
            ""
        ).strip()

        department = request.POST.get(
            "department",
            ""
        ).strip()

        designation = request.POST.get(
            "designation",
            ""
        ).strip()

        # -------------------------------------------------
        # Required field validation
        # -------------------------------------------------

        if (
            not username
            or not email
            or not password
            or not employee_id
        ):

            error = (
                "Please fill all required fields."
            )

        # -------------------------------------------------
        # Username validation
        # -------------------------------------------------

        elif User.objects.filter(
            username=username
        ).exists():

            error = (
                "Username already exists."
            )

        # -------------------------------------------------
        # Employee ID validation
        # -------------------------------------------------

        elif UserProfile.objects.filter(
            employee_id=employee_id
        ).exists():

            error = (
                "Employee ID already exists."
            )

        else:

            # -------------------------------------------------
            # Create Django User
            # -------------------------------------------------

            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )

            # -------------------------------------------------
            # Signal automatically creates UserProfile
            # -------------------------------------------------

            profile = user.profile

            profile.role = "EMPLOYEE"

            profile.employee_id = employee_id

            profile.department = department

            profile.designation = designation

            profile.save()

            return redirect(
                "employee_list"
            )

    return render(
        request,
        "add_employee.html",
        {
            "error": error
        }
    )

@login_required(login_url="user_login")
def hr_documents(request):
    if request.user.profile.role != "HR":
        return redirect("employee_dashboard")

    error = None
    success = None

    if request.method == "POST":
        title = request.POST.get("title", "").strip()
        uploaded_file = request.FILES.get("file")

        if not title:
            error = "Please enter a document title."

        elif not uploaded_file:
            error = "Please select a document."

        else:
            allowed_extensions = [".pdf", ".docx", ".txt", ".md"]

            filename = uploaded_file.name.lower()

            if not any(filename.endswith(ext) for ext in allowed_extensions):
                error = (
                    "Unsupported file type. "
                    "Only PDF, DOCX, TXT, and MD files are allowed."
                )

            else:
                try:
                    document = HRDocument.objects.create(
                        title=title,
                        file=uploaded_file,
                        uploaded_by=request.user
                    )

                    file_path = document.file.path

                    extracted_text = extract_text_from_file(
                        file_path
                    )

                    if not extracted_text.strip():
                        document.delete()

                        error = (
                            "Could not extract text from this document."
                        )

                    else:
                        chunk_count = process_document(
                            document,
                            extracted_text
                        )

                        if chunk_count == 0:
                            document.delete()

                            error = (
                                "No usable text was found in the document."
                            )

                        else:
                            success = (
                                f"Document uploaded successfully. "
                                f"{chunk_count} chunks created."
                            )

                except Exception as e:
                    print("Document upload error:", e)

                    if "document" in locals():
                        document.delete()

                    error = (
                        "An error occurred while processing "
                        "the document."
                    )

    documents = HRDocument.objects.order_by("-uploaded_at")

    return render(
        request,
        "hr_documents.html",
        {
            "documents": documents,
            "error": error,
            "success": success,
        }
    )
@login_required(login_url="user_login")
def delete_hr_document(request, document_id):
    if request.user.profile.role != "HR":
        return redirect("employee_dashboard")

    if request.method == "POST":
        document = get_object_or_404(
            HRDocument,
            id=document_id
        )

        document.delete()

    return redirect("hr_documents")