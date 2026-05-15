import json


def build_report(domain, whois, dns, ip, web, enrich, corr, anomaly, graph):
    return {
        "target": domain,
        "whois": whois,
        "dns": dns,
        "ip_asn": ip,
        "website": web,
        "enrichment": enrich,
        "correlation": corr,
        "anomaly": anomaly,
        "graph": graph
    }


def export_json(report, filename="report.json"):
    with open(filename, "w") as f:
        json.dump(report, f, indent=2)
