import socket
import requests


def resolve_ip(domain):
    try:
        return socket.gethostbyname(domain)
    except Exception:
        return None


def get_ip_info(ip):
    try:
        r = requests.get(f"https://ipinfo.io/{ip}/json", timeout=5)
        return r.json()
    except Exception:
        return {}


def ip_asn_info(domain):
    ip = resolve_ip(domain)

    if not ip:
        return {
            "domain": domain,
            "error": "Could not resolve IP"
        }

    info = get_ip_info(ip)

    return {
        "domain": domain,
        "ip": ip,
        "hostname": info.get("hostname"),
        "city": info.get("city"),
        "region": info.get("region"),
        "country": info.get("country"),
        "org": info.get("org"),
        "asn": info.get("org"),
        "location": f"{info.get('city')}, {info.get('country')}"
    }
