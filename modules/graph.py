def build_graph(domain, ip_data, dns_data, subs):
    nodes = []
    edges = []

    nodes.append({"id": domain, "type": "domain"})

    ip = ip_data.get("ip")
    if ip:
        nodes.append({"id": ip, "type": "ip"})
        edges.append({"from": domain, "to": ip, "type": "resolves_to"})

    for ns in dns_data.get("NS", []):
        nodes.append({"id": ns, "type": "nameserver"})
        edges.append({"from": domain, "to": ns, "type": "uses_ns"})

    for s in subs:
        nodes.append({"id": s, "type": "subdomain"})
        edges.append({"from": domain, "to": s, "type": "subdomain"})

    return {
        "nodes": nodes,
        "edges": edges
    }
