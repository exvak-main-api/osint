import dns.resolver


def _resolve(domain, record_type):
    try:
        answers = dns.resolver.resolve(domain, record_type)
        return [r.to_text() for r in answers]
    except Exception:
        return []


def get_dns(domain):
    return {
        "A": _resolve(domain, "A"),
        "AAAA": _resolve(domain, "AAAA"),
        "MX": _resolve(domain, "MX"),
        "TXT": _resolve(domain, "TXT"),
        "NS": _resolve(domain, "NS"),
        "CNAME": _resolve(domain, "CNAME"),
        "SOA": _resolve(domain, "SOA"),
    }
