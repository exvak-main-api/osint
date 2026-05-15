def correlate(domain, whois_data, dns_data, ip_data):
    score = 0
    signals = []

    def add(points, msg):
        nonlocal score
        score += points
        signals.append(msg)

    age = whois_data.get("age_days")
    if isinstance(age, int):
        if age < 30:
            add(40, "Very new domain")
        elif age < 365:
            add(20, "New domain")

    if whois_data.get("privacy_protected") is True:
        add(20, "WHOIS privacy enabled")

    exp = whois_data.get("expires_in_days")
    if isinstance(exp, int):
        if exp < 0:
            add(30, "Domain expired")
        elif exp < 30:
            add(20, "Expiring soon")

    if not dns_data.get("has_mx"):
        add(15, "No MX records")

    if not dns_data.get("has_spf"):
        add(10, "No SPF record")

    if not dns_data.get("has_dmarc"):
        add(10, "No DMARC record")

    ns = dns_data.get("NS") or []
    if len(ns) <= 2:
        add(5, "Low nameserver diversity")

    org = (ip_data.get("org") or "").lower()

    infra_map = {
        "cloudflare": "Cloudflare protection detected",
        "amazon": "AWS hosting detected",
        "aws": "AWS hosting detected",
        "google": "Google infrastructure detected"
    }

    for key, msg in infra_map.items():
        if key in org:
            signals.append(msg)

    if ip_data.get("ip"):
        signals.append(f"Resolved IP: {ip_data['ip']}")

    return {
        "risk_score": max(0, min(score, 100)),
        "signals": signals
    }
