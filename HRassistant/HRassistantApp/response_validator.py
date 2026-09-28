import re


def validate_response(response):
    warnings = []

    # Check for email addresses
    if re.search(
        r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",
        response,
        re.IGNORECASE
    ):
        warnings.append("Email address detected")

    # Check for 10-digit phone numbers
    if re.search(r"\b\d{10}\b", response):
        warnings.append("Phone number detected")

    # Check for Aadhaar-like 12-digit numbers
    if re.search(r"\b\d{4}\s?\d{4}\s?\d{4}\b", response):
        warnings.append("Potential ID number detected")

    # Check for sensitive information
    sensitive_patterns = [
        r"\bpassword\b",
        r"\bsecret\s+key\b",
        r"\bapi\s+key\b",
        r"\baccess\s+token\b",
        r"\bauthentication\s+token\b",
    ]

    for pattern in sensitive_patterns:
        if re.search(pattern, response, re.IGNORECASE):
            warnings.append("Sensitive information detected")
            break

    # Return validation result
    if warnings:
        return {
            "is_safe": False,
            "warnings": warnings,
            "message": "Response requires security review."
        }

    return {
        "is_safe": True,
        "warnings": [],
        "message": "Response passed security validation."
    }