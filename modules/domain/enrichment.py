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
            name = entry.get("name_value", "")
            for sub in name.split("\n"):
                sub = sub.strip().lower()
                if sub.endswith(domain):
                    subs.add(sub)

        return sorted(list(subs))

    except:
        return []


def validate_subdomains(subdomains):
    valid = []

    for sub in subdomains:
        try:
            socket.gethostbyname(sub)
            valid.append(sub)
        except:
            continue

    return valid


def reverse_ip_lookup(domain):
    try:
        ip = socket.gethostbyname(domain)

        url = f"https://api.hackertarget.com/reverseiplookup/?q={ip}"
        r = requests.get(url, timeout=10)

        if r.status_code != 200:
            return {"ip": ip, "domains": []}

        domains = r.text.splitlines()
        domains = [d for d in domains if "." in d]

        return {
            "ip": ip,
            "domains": domains
        }

    except:
        return {"ip": None, "domains": []}
