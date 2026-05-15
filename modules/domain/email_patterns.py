import re


COMMON_PATTERNS = [
    "first.last",
    "first_last",
    "firstlast",
    "f.last",
    "firstl",
    "first",
    "last",
    "flast",
    "first.last123"
]


ROLE_ACCOUNTS = [
    "admin",
    "info",
    "support",
    "contact",
    "sales",
    "hello",
    "security",
    "help",
    "service",
    "team",
    "billing"
]


def extract_domain(email):
    try:
        return email.split("@")[1].lower()
    except:
        return None


def generate_patterns(domain):
    return [f"{p}@{domain}" for p in COMMON_PATTERNS]


def role_accounts(domain):
    return [f"{r}@{domain}" for r in ROLE_ACCOUNTS]


def detect_company_style(emails):
    """
    Infers pattern style from leaked emails (if provided)
    """
    patterns = set()

    for email in emails:
        try:
            local, domain = email.lower().split("@")

            if "." in local:
                patterns.add("first.last style")
            if "_" in local:
                patterns.add("underscore style")
            if local[0].isalpha() and len(local) <= 2:
                patterns.add("initial-based style")
            if any(char.isdigit() for char in local):
                patterns.add("numbered accounts")
        except:
            continue

    return list(patterns)


def email_intel(domain, sample_emails=None):
    return {
        "domain": domain,
        "patterns": generate_patterns(domain),
        "role_accounts": role_accounts(domain),
        "detected_style": detect_company_style(sample_emails or [])
    }
