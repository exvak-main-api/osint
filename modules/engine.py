from modules.graph import build_graph
from modules.scoring import compute_score
from modules.report import build_report, export_json


def run_engine(domain, whois, dns, ip, web, enrich, corr, anomaly, subs):

    graph = build_graph(domain, ip, dns, subs)

    score = compute_score(corr, anomaly)

    report = build_report(
        domain,
        whois,
        dns,
        ip,
        web,
        enrich,
        corr,
        anomaly,
        graph
    )

    report["score"] = score
    report["graph"] = graph

    export_json(report)

    return report
