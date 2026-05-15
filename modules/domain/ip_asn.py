import requests
import socket


IP_API = "https://ipapi.co/{}/json/"


def resolve_ip(target):
    try:
        return socket.gethostbyname(target)
    except:
        return None


def fetch_ip_data(ip):
    try:
        r = requests.get(IP_API.format(ip), timeout=8)
        if r.status_code != 200:
            return {}

        d = r.json()

        return {
            "ip": ip,
            "city": d.get("city"),
            "region": d.get("region"),
            "country": d.get("country_code"),
            "country_name": d.get("country_name"),
            "latitude": d.get("latitude"),
            "longitude": d.get("longitude"),
            "timezone": d.get("timezone"),
            "asn": d.get("asn"),
            "org": d.get("org"),
            "network": d.get("network"),
            "version": d.get("version"),
            "country_area": d.get("country_area"),
            "country_population": d.get("country_population"),
            "currency": d.get("currency"),
        }

    except:
        return {}


def detect_infrastructure(org):
    if not org:
        return []

    org = org.lower()
    signals = []

    if "cloudflare" in org:
        signals.append("Cloudflare CDN detected")

    if "amazon" in org or "aws" in org:
        signals.append("AWS hosting detected")

    if "google" in org:
        signals.append("Google Cloud infrastructure detected")

    if "microsoft" in org or "azure" in org:
        signals.append("Microsoft Azure hosting detected")

    if "digitalocean" in org:
        signals.append("DigitalOcean VPS detected")

    if "ovh" in org:
        signals.append("OVH hosting detected")

    return signals


def ip_asn_info(domain):
    try:
        ip = resolve_ip(domain)

        if not ip:
            return {
                "error": "DNS resolution failed"
            }

        data = fetch_ip_data(ip)

        infra = detect_infrastructure(data.get("org"))

        return {
            "ip": ip,
            "asn": data.get("asn"),
            "org": data.get("org"),
            "network": data.get("network"),
            "city": data.get("city"),
            "region": data.get("region"),
            "country": data.get("country"),
            "country_name": data.get("country_name"),
            "timezone": data.get("timezone"),
            "latitude": data.get("latitude"),
            "longitude": data.get("longitude"),
            "currency": data.get("currency"),
            "version": data.get("version"),
            "infrastructure": infra,
            "raw": data
        }

    except:
        return {
            "error": True
        }
