import re


def guess_patterns(domain):
    domain = domain.lower()

    patterns = [
        f"firstname.lastname@{domain}",
        f"first.last@{domain}",
        f"firstname_lastname@{domain}",
        f"f.lastname@{domain}",
        f"firstname@{domain}",
        f"lastname@{domain}",
        f"flastname@{domain}",
    ]

    return patterns


def extract_emails_from_text(text):
    try:
        return list(set(re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text)))
    except Exception:
        return []
