import re


def scan_prompt(message):
    message = message.lower().strip()

    high_risk_patterns = {
        "Ignore previous instructions": r"ignore\s+(all\s+)?previous\s+instructions",
        "Reveal system prompt": r"(reveal|show|tell|give).*(system\s+prompt|hidden\s+instructions)",
        "Bypass security": r"(bypass|disable|circumvent).*(security|restriction|protection)",
        "Reveal password": r"(reveal|show|give|tell me).*(password|secret|api\s*key)",
        "Role manipulation": r"you\s+are\s+now",
    }

    medium_risk_patterns = {
        "Employee personal information": (
            r"(show|give|tell me|reveal).*(employee\s+data|personal\s+information)"
        ),
        "Confidential information": (
            r"(show|give|reveal|tell me).*(confidential|private\s+information)"
        ),
        "Employee salary information": (
            r"(show|give|tell me|reveal).*(employee\s+salary|salary\s+details)"
        ),
    }

    dangerous_request_patterns = {
        "Credential theft": (
            r"(steal|capture|harvest|collect).*(password|credential|login)"
        ),
        "Malware request": (
            r"(create|write|make|build).*(malware|ransomware|keylogger)"
        ),
        "Unauthorized access": (
            r"(hack|break into|gain access to).*(account|server|system|computer)"
        ),
    }

    matched_rules = []

    # High-risk prompt injection/security patterns
    for rule_name, pattern in high_risk_patterns.items():
        if re.search(pattern, message, re.IGNORECASE):
            matched_rules.append(rule_name)

    if matched_rules:
        return {
            "is_suspicious": True,
            "risk_level": "High",
            "matched_rules": matched_rules,
            "message": "High-risk instruction detected.",
        }

    # Dangerous request patterns
    for rule_name, pattern in dangerous_request_patterns.items():
        if re.search(pattern, message, re.IGNORECASE):
            matched_rules.append(rule_name)

    if matched_rules:
        return {
            "is_suspicious": True,
            "risk_level": "High",
            "matched_rules": matched_rules,
            "message": "Potentially dangerous request detected.",
        }

    # Medium-risk patterns
    for rule_name, pattern in medium_risk_patterns.items():
        if re.search(pattern, message, re.IGNORECASE):
            matched_rules.append(rule_name)

    if matched_rules:
        return {
            "is_suspicious": True,
            "risk_level": "Medium",
            "matched_rules": matched_rules,
            "message": "Medium-risk instruction detected.",
        }

    # Normal prompt
    return {
        "is_suspicious": False,
        "risk_level": "Low",
        "matched_rules": [],
        "message": "No suspicious instruction detected.",
    }


def mask_sensitive_data(message):

    # Mask email addresses
    message = re.sub(
        r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",
        "[EMAIL PROTECTED]",
        message,
    )

    # Mask 10-digit phone numbers
    message = re.sub(
        r"\b\d{10}\b",
        "[PHONE NUMBER PROTECTED]",
        message,
    )

    # Mask 12-digit Aadhaar-like numbers
    message = re.sub(
        r"\b\d{4}\s?\d{4}\s?\d{4}\b",
        "[ID NUMBER PROTECTED]",
        message,
    )

    return message