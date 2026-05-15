def detect_anomalies(domain, whois_data, dns_data, ip_data):
    anomalies = []
    score = 0

    def add(points, msg):
        nonlocal score
        score += points
        anomalies.append(msg)

    country = (ip_data.get("country") or "").lower()
    org = (ip_data.get("org") or "").lower()
    registrar = (whois_data.get("registrar") or "").lower()

    if country and "cloudflare" in registrar:
        add(15, "Geo + registrar mismatch signal")

    if not dns_data.get("has_mx") and not dns_data.get("has_spf") and "cloudflare" in org:
        add(20, "Cloudflare with no email infrastructure")

    age = whois_data.get("age_days")
    if isinstance(age, int) and age < 7 and ("aws" in org or "google" in org):
        add(25, "Very new domain on major cloud provider")

    ns = dns_data.get("NS") or []
    if len(ns) == 0:
        add(30, "No nameservers detected")
    elif len(ns) == 1:
        add(10, "Single nameserver detected")

    missing = 0
    if not dns_data.get("has_mx"):
        missing += 1
    if not dns_data.get("has_spf"):
        missing += 1
    if not dns_data.get("has_dmarc"):
        missing += 1

    if missing == 3:
        add(35, "Complete email security absence")
    elif missing == 2:
        add(20, "Weak email security posture")

    infra = 0
    for x in ["cloudflare", "aws", "google", "azure", "digitalocean", "ovh"]:
        if x in org:
            infra += 1

    if infra == 0:
        add(10, "No major infrastructure provider detected")

    score = max(0, min(score, 100))

    if score >= 60:
        level = "HIGH ANOMALY"
    elif score >= 30:
        level = "MEDIUM ANOMALY"
    else:
        level = "LOW ANOMALY"

    return {
        "anomaly_score": score,
        "anomaly_level": level,
        "anomalies": anomalies
    }
