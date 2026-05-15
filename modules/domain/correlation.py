def correlate(domain, whois_data, dns_data, ip_data):
    score = 0
    signals = []

    age = whois_data.get("age_days")
    if age is not None:
        if age < 30:
            score += 40
            signals.append("Very new domain")
        elif age < 365:
            score += 20
            signals.append("New domain")

    if whois_data.get("privacy_protected"):
        score += 20
        signals.append("WHOIS privacy enabled")

    expires = whois_data.get("expires_in_days")
    if expires is not None:
        if expires < 30:
            score += 20
            signals.append("Expiring soon")
        if expires < 0:
            score += 30
            signals.append("Domain expired")

    mx = dns_data.get("MX", [])
    ns = dns_data.get("NS", [])

    if not mx:
        score += 10
        signals.append("No MX records")

    if ns and len(ns) <= 2:
        score += 5
        signals.append("Low nameserver diversity")

    org = ip_data.get("org") or ""

    if "cloudflare" in org.lower():
        signals.append("Cloudflare protection detected")

    if "amazon" in org.lower() or "aws" in org.lower():
        signals.append("AWS hosting detected")

    if "google" in org.lower():
        signals.append("Google infrastructure detected")

    return {
        "risk_score": min(score, 100),
        "signals": signals
    }
