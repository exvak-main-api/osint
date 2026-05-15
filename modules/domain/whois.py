from datetime import datetime, timezone
import whois


def _safe_datetime(value):
    if not value:
        return None

    if isinstance(value, list):
        value = value[0]

    if isinstance(value, datetime):
        return value if value.tzinfo else value.replace(tzinfo=timezone.utc)

    try:
        if isinstance(value, str):
            value = value.replace("Z", "+00:00")
            dt = datetime.fromisoformat(value)
            return dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)
    except:
        return None

    return None


def domain_whois(domain):
    try:
        w = whois.whois(domain)

        creation = _safe_datetime(getattr(w, "creation_date", None))
        expiration = _safe_datetime(getattr(w, "expiration_date", None))
        updated = _safe_datetime(getattr(w, "updated_date", None))

        now = datetime.now(timezone.utc)

        age_days = None
        expires_in_days = None

        if creation:
            age_days = (now - creation).days

        if expiration:
            expires_in_days = (expiration - now).days

        privacy = False
        raw = str(w.text).lower() if hasattr(w, "text") else ""

        if "privacy" in raw or "redacted" in raw or "whoisguard" in raw:
            privacy = True

        return {
            "domain": domain,
            "registrar": getattr(w, "registrar", None),
            "status": getattr(w, "status", None),
            "name_servers": getattr(w, "name_servers", None),

            "creation_date": creation.isoformat() if creation else None,
            "expiration_date": expiration.isoformat() if expiration else None,
            "updated_date": updated.isoformat() if updated else None,

            "age_days": age_days,
            "expires_in_days": expires_in_days,
            "privacy_protected": privacy
        }

    except Exception as e:
        return {
            "domain": domain,
            "error": str(e)
        }
