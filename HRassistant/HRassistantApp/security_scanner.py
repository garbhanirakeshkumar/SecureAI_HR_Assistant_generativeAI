import re


def scan_prompt(message):

    message = message.lower().strip()

    # =====================================================
    # HIGH-RISK PATTERNS
    # =====================================================

    high_risk_patterns = {

        "Ignore previous instructions":
            r"ignore\s+(all\s+)?previous\s+instructions",

        "Reveal system prompt":
            r"(reveal|show|tell|give).*\b(system\s+prompt|hidden\s+instructions)\b",

        "Bypass security":
            r"(bypass|disable|circumvent).*\b(security|restriction|protection)\b",

        "Reveal password":
            r"(reveal|show|give|tell\s+me).*\b(password|secret|api\s+key)\b",

        "Role manipulation":
            r"you\s+are\s+now",
    }


    # =====================================================
    # MEDIUM-RISK PATTERNS
    # =====================================================

    medium_risk_patterns = {

        "Employee personal information":
            r"(show|give|tell\s+me|reveal).*\b(employee\s+data|personal\s+information)\b",

        "Confidential information":
            r"(show|give|reveal|tell\s+me).*\b(confidential|private\s+information)\b",

        "Employee salary information":
            r"(show|give|tell\s+me|reveal).*\b(employee\s+salary|salary\s+details)\b",
    }


    # =====================================================
    # DANGEROUS REQUEST PATTERNS
    # =====================================================

    dangerous_request_patterns = {

        "Credential theft":
            r"(steal|capture|harvest|collect).*\b(password|credential|login)\b",

        "Malware request":
            r"(create|write|make|build).*\b(malware|ransomware|keylogger)\b",

        "Unauthorized access":
            r"(hack|break\s+into|gain\s+access\s+to).*\b(account|server|system|computer)\b",
    }


    matched_rules = []


    # =====================================================
    # 1. HIGH-RISK PROMPT INJECTION
    # =====================================================

    for rule_name, pattern in high_risk_patterns.items():

        if re.search(
            pattern,
            message,
            re.IGNORECASE
        ):
            matched_rules.append(rule_name)


    if matched_rules:

        return {
            "is_suspicious": True,
            "risk_level": "High",
            "matched_rules": matched_rules,
            "message": "High-risk instruction detected.",
        }


    # =====================================================
    # 2. DANGEROUS REQUESTS
    # =====================================================

    for rule_name, pattern in dangerous_request_patterns.items():

        if re.search(
            pattern,
            message,
            re.IGNORECASE
        ):
            matched_rules.append(rule_name)


    if matched_rules:

        return {
            "is_suspicious": True,
            "risk_level": "High",
            "matched_rules": matched_rules,
            "message": "Potentially dangerous request detected.",
        }


    # =====================================================
    # 3. MEDIUM-RISK REQUESTS
    # =====================================================

    for rule_name, pattern in medium_risk_patterns.items():

        if re.search(
            pattern,
            message,
            re.IGNORECASE
        ):
            matched_rules.append(rule_name)


    if matched_rules:

        return {
            "is_suspicious": True,
            "risk_level": "Medium",
            "matched_rules": matched_rules,
            "message": "Medium-risk instruction detected.",
        }


    # =====================================================
    # 4. NORMAL PROMPT
    # =====================================================

    return {
        "is_suspicious": False,
        "risk_level": "Low",
        "matched_rules": [],
        "message": "No suspicious instruction detected.",
    }


# =========================================================
# MASK SENSITIVE DATA
# =========================================================

def mask_sensitive_data(message):

    # -----------------------------------------------------
    # Mask email addresses
    # -----------------------------------------------------

    message = re.sub(
        r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",
        "[EMAIL PROTECTED]",
        message,
        flags=re.IGNORECASE
    )


    # -----------------------------------------------------
    # Mask 10-digit phone numbers
    # -----------------------------------------------------

    message = re.sub(
        r"\b\d{10}\b",
        "[PHONE NUMBER PROTECTED]",
        message
    )


    # -----------------------------------------------------
    # Mask 12-digit Aadhaar-like numbers
    # -----------------------------------------------------

    message = re.sub(
        r"\b\d{4}\s?\d{4}\s?\d{4}\b",
        "[ID NUMBER PROTECTED]",
        message
    )


    return message