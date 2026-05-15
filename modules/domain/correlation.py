from modules.domain.anomaly import detect_anomalies


def correlate(domain, whois_data, dns_data, ip_data):
    score = 0
    signals = []

    def add(points, msg):
        nonlocal score
        score += points
        signals.append(msg)

    age = whois_data.get("age_days")
    if isinstance(age, int):
        if age < 7:
            add(60, "Extremely new domain")
        elif age < 30:
            add(40, "Very new domain")
        elif age < 180:
            add(20, "New domain")

    if whois_data.get("privacy_protected"):
        add(20, "WHOIS privacy enabled")

    exp = whois_data.get("expires_in_days")
    if isinstance(exp, int):
        if exp < 0:
            add(50, "Domain expired")
        elif exp < 15:
            add(35, "Domain expiring immediately")
        elif exp < 60:
            add(15, "Domain expiring soon")

    registrar = (whois_data.get("registrar") or "").lower()
    if registrar:
        if any(x in registrar for x in ["namecheap", "godaddy", "porkbun", "gandi"]):
            add(5, "Mass-market registrar detected")

    if not dns_data.get("has_mx"):
        add(20, "No MX records")

    if not dns_data.get("has_spf"):
        add(10, "No SPF record")

    if not dns_data.get("has_dmarc"):
        add(10, "No DMARC record")

    ns = dns_data.get("NS") or []
    if len(ns) <= 2:
        add(5, "Low nameserver diversity")

    if dns_data.get("mx_count", 0) <= 1 and dns_data.get("has_mx"):
        add(5, "Low MX redundancy")

    org = (ip_data.get("org") or "").lower()

    infra_map = {
        "cloudflare": "Cloudflare detected",
        "aws": "AWS detected",
        "amazon": "AWS detected",
        "google": "Google Cloud detected",
        "microsoft": "Azure detected",
        "azure": "Azure detected",
        "digitalocean": "DigitalOcean detected",
        "ovh": "OVH detected"
    }

    for k, v in infra_map.items():
        if k in org:
            signals.append(v)

    ip = ip_data.get("ip")
    if ip:
        signals.append(f"Resolved IP: {ip}")
    else:
        add(10, "No IP resolution")

    anomaly = detect_anomalies(domain, whois_data, dns_data, ip_data)

    score = max(0, min(score, 100))

    if score >= 70:
        level = "HIGH RISK"
    elif score >= 40:
        level = "MEDIUM RISK"
    else:
        level = "LOW RISK"

    return {
        "risk_score": score,
        "risk_level": level,
        "signals": signals,
        "anomaly": anomaly
    }
