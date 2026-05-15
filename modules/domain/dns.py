import socket
import dns.resolver


def _query(domain, record):
    try:
        answers = dns.resolver.resolve(domain, record, raise_on_no_answer=False)
        return [str(r).strip() for r in answers]
    except:
        return []


def _ip(domain):
    try:
        return socket.gethostbyname(domain)
    except:
        return None


def dns_lookup(domain):
    try:
        data = {
            "domain": domain,
            "A": _query(domain, "A"),
            "AAAA": _query(domain, "AAAA"),
            "MX": _query(domain, "MX"),
            "NS": _query(domain, "NS"),
            "TXT": _query(domain, "TXT"),
            "CNAME": _query(domain, "CNAME"),
            "SOA": _query(domain, "SOA"),
            "SRV": _query(domain, "SRV"),
            "ip": None,
            "mail_servers": [],
            "has_mx": False,
            "has_spf": False,
            "has_dmarc": False
        }

        data["ip"] = _ip(domain)

        if data["MX"]:
            data["mail_servers"] = [m.split()[-1].rstrip(".") for m in data["MX"]]
            data["has_mx"] = True

        for t in data["TXT"]:
            tl = t.lower()
            if "v=spf1" in tl:
                data["has_spf"] = True
            if "dmarc" in tl:
                data["has_dmarc"] = True

        return data

    except:
        return {
            "domain": domain,
            "error": True
        }
