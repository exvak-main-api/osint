import socket


def enrich_subdomains(subs):
    enriched = []

    for s in subs:
        try:
            ip = socket.gethostbyname(s)
            enriched.append({
                "subdomain": s,
                "ip": ip
            })
        except:
            enriched.append({
                "subdomain": s,
                "ip": None
            })

    return enriched
