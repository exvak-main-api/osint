import re
from lib.colors import *
from lib.update import Version_Checker

from modules.domain import (
    domain_whois,
    dns_lookup,
    ip_asn_info,
    website_info,
    enrichment_report,
    crt_subdomains,
    validate_subdomains,
    reverse_ip_lookup,
    correlate,
    detect_anomalies
)

from modules.username import username_osint
from modules.domain.email_patterns import email_intel
from modules.engine import run_engine
from modules.subdomains import enrich_subdomains


EMAIL_REGEX = re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}')


def banner():
    print(f"""{GREEN}
=====================================
        EXVAK OSINT PANEL
=====================================
{WHITE}""")


def section(title):
    print(f"\n{YELLOW}==== {title.upper()} ===={WHITE}")


def safe(fn, *args):
    try:
        return fn(*args)
    except:
        return None


async def parser():

    await safe(Version_Checker().checker)

    banner()

    print(f"{YELLOW}[1]{WHITE} Email OSINT")
    print(f"{YELLOW}[2]{WHITE} Phone OSINT")
    print(f"{YELLOW}[3]{WHITE} Domain OSINT")
    print(f"{YELLOW}[4]{WHITE} Username OSINT")
    print(f"{YELLOW}[0]{WHITE} Exit\n")

    choice = input(f"{YELLOW}Select > {WHITE}").strip()

    if choice == "0":
        return

    if choice == "1":

        email = input(f"{YELLOW}Email > {WHITE}").strip()

        if not EMAIL_REGEX.match(email):
            return

        domain = email.split("@")[-1]

        section("EMAIL INTELLIGENCE")

        data = safe(email_intel, domain)
        if data:
            print(data)

        return

    if choice == "2":

        phone = input(f"{YELLOW}Phone > {WHITE}").strip()

        section("PHONE")

        print(phone)

        return

    if choice == "3":

        domain = input(f"{YELLOW}Domain > {WHITE}").strip()

        section("DOMAIN INTELLIGENCE")

        whois = safe(domain_whois, domain)
        dns = safe(dns_lookup, domain)
        ip = safe(ip_asn_info, domain)
        web = safe(website_info, domain)
        enrich = safe(enrichment_report, domain)

        corr = safe(correlate, domain, whois, dns, ip)
        anomaly = safe(detect_anomalies, domain, whois, dns, ip)

        subs = safe(crt_subdomains, domain)
        valid = []
        if subs:
            valid, _ = validate_subdomains(subs)

        graph_subs = enrich_subdomains(valid) if valid else []

        report = safe(
            run_engine,
            domain,
            whois,
            dns,
            ip,
            web,
            enrich,
            corr,
            anomaly,
            valid
        )

        section("WHOIS")
        print(whois)

        section("DNS")
        print(dns)

        section("IP / ASN")
        print(ip)

        section("WEBSITE")
        print(web)

        section("ENRICHMENT")
        print(enrich)

        section("CORRELATION")
        print(corr)

        section("ANOMALY")
        print(anomaly)

        section("SUBDOMAINS")
        print(valid)

        section("REVERSE IP")
        print(reverse_ip_lookup(domain))

        section("GRAPH")
        print(report["graph"] if report else None)

        section("SCORE")
        print(report["score"] if report else None)

        return

    if choice == "4":

        username = input(f"{YELLOW}Username > {WHITE}").strip()

        section("USERNAME OSINT")

        print(safe(username_osint, username))

        return

    print(f"{RED}Invalid option{WHITE}")
