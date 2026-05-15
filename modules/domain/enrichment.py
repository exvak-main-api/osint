import requests
import socket


def crt_subdomains(domain):
    try:
        url = f"https://crt.sh/?q=%25.{domain}&output=json"
        r = requests.get(url, timeout=10)

        if r.status_code != 200:
            return []

        data = r.json()
        subs = set()

        for entry in data:
            names = entry.get("name_value", "")
            for n in names.split("\n"):
                n = n.strip().lower()
                if n.endswith(domain):
                    subs.add(n)

        return sorted(list(subs))

    except:
        return []


def resolve_domain(domain):
    try:
        return socket.gethostbyname(domain)
    except:
        return None


def validate_subdomains(subdomains):
    valid = []
    resolved = {}

    for sub in subdomains:
        try:
            ip = socket.gethostbyname(sub)
            valid.append(sub)
            resolved[sub] = ip
        except:
            continue

    return valid, resolved


def reverse_ip_lookup(domain):
    try:
        ip = resolve_domain(domain)

        if not ip:
            return {
                "ip": None,
                "domains": [],
                "error": "DNS resolution failed"
            }

        url = f"https://api.hackertarget.com/reverseiplookup/?q={ip}"
        r = requests.get(url, timeout=10)

        domains = []

        if r.status_code == 200:
            domains = [d.strip() for d in r.text.splitlines() if "." in d]

        return {
            "ip": ip,
            "domains": domains
        }

    except:
        return {
            "ip": None,
            "domains": [],
            "error": True
        }


def dns_enrichment(domain):
    try:
        import dns.resolver

        def q(t):
            try:
                return [str(r) for r in dns.resolver.resolve(domain, t)]
            except:
                return []

        mx = q("MX")
        ns = q("NS")
        txt = q("TXT")

        spf = any("v=spf1" in t.lower() for t in txt)
        dmarc = any("dmarc" in t.lower() for t in txt)

        return {
            "MX": mx,
            "NS": ns,
            "TXT": txt,
            "has_mx": bool(mx),
            "has_spf": spf,
            "has_dmarc": dmarc,
            "nameserver_count": len(ns),
            "mx_count": len(mx)
        }

    except:
        return {
            "MX": [],
            "NS": [],
            "TXT": [],
            "has_mx": False,
            "has_spf": False,
            "has_dmarc": False,
            "nameserver_count": 0,
            "mx_count": 0,
            "error": True
        }


def enrichment_report(domain):
    try:
        subs = crt_subdomains(domain)
        valid_subs, resolved = validate_subdomains(subs)
        rev = reverse_ip_lookup(domain)
        dns = dns_enrichment(domain)

        return {
            "domain": domain,
            "subdomains": {
                "all": subs,
                "valid": valid_subs,
                "resolved": resolved,
                "count": len(valid_subs)
            },
            "reverse_ip": rev,
            "dns": dns
        }

    except:
        return {
            "domain": domain,
            "error": True
        }
