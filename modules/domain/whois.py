import whois
from datetime import datetime

def _safe_date(value):
    if isinstance(value, list):
        value = value[0] if value else None
    return value

def _days_between(d1, d2):
    return (d2 - d1).days


def get_whois(domain):
    try:
        w = whois.whois(domain)
        now = datetime.utcnow()

        creation_date = _safe_date(w.creation_date)
        expiration_date = _safe_date(w.expiration_date)

        age_days = None
        if creation_date:
            age_days = _days_between(creation_date, now)

        expires_in_days = None
        if expiration_date:
            expires_in_days = _days_between(now, expiration_date)

        raw = str(w).lower()

        privacy = any(x in raw for x in [
            "redacted", "privacy", "whoisguard", "proxy", "private"
        ])

        ns = w.name_servers
        if isinstance(ns, str):
            ns = [ns]
        if ns is None:
            ns = []

        emails = w.emails
        if isinstance(emails, str):
            emails = [emails]
        if emails is None:
            emails = []

        flags = []

        if privacy:
            flags.append("privacy_protected")

        if age_days is not None:
            if age_days < 30:
                flags.append("very_new_domain")
            elif age_days < 365:
                flags.append("new_domain")

        if expires_in_days is not None:
            if expires_in_days < 30:
                flags.append("expiring_soon")
            if expires_in_days < 0:
                flags.append("expired_domain")

        risk = 0

        if age_days is not None:
            if age_days < 30:
                risk += 40
            elif age_days < 365:
                risk += 20

        if privacy:
            risk += 20

        if expires_in_days is not None:
            if expires_in_days < 30:
                risk += 20
            if expires_in_days < 0:
                risk += 30

        risk = min(risk, 100)

        return {
            "domain": domain,
            "registrar": w.registrar,
            "creation_date": str(creation_date) if creation_date else None,
            "expiration_date": str(expiration_date) if expiration_date else None,
            "age_days": age_days,
            "expires_in_days": expires_in_days,
            "privacy_protected": privacy,
            "name_servers": ns,
            "emails": emails,
            "flags": flags,
            "risk_score": risk
        }

    except Exception as e:
        return {
            "domain": domain,
            "error": str(e)
        }
