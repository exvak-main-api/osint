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
from modules.email_patterns import email_intel


EMAIL_REGEX = re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}')


def header():
    print(f"""{GREEN}
=====================================
        EXVAK OSINT PANEL
=====================================
{WHITE}""")


async def parser():

    try:
        await Version_Checker().checker()
    except:
        pass

    header()

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

        data = email_intel(domain)

        print("\nEMAIL INTEL")
        print(data)

        return

    if choice == "2":

        phone = input(f"{YELLOW}Phone > {WHITE}").strip()

        print("\nPHONE")
        print(phone)

        return

    if choice == "3":

        domain = input(f"{YELLOW}Domain > {WHITE}").strip()

        print(f"\nDOMAIN: {domain}\n")

        whois = domain_whois(domain)
        dns = dns_lookup(domain)
        ip = ip_asn_info(domain)
        web = website_info(domain)
        enrich = enrichment_report(domain)

        corr = correlate(domain, whois, dns, ip)
        anomaly = detect_anomalies(domain, whois, dns, ip)

        subs = crt_subdomains(domain)
        valid, _ = validate_subdomains(subs)
        rev = reverse_ip_lookup(domain)

        print("\nWHOIS")
        print(whois)

        print("\nDNS")
        print(dns)

        print("\nIP / ASN")
        print(ip)

        print("\nWEBSITE")
        print(web)

        print("\nENRICHMENT")
        print(enrich)

        print("\nCORRELATION")
        print(corr)

        print("\nANOMALY")
        print(anomaly)

        print("\nSUBDOMAINS")
        print(valid)

        print("\nREVERSE IP")
        print(rev)

        return

    if choice == "4":

        username = input(f"{YELLOW}Username > {WHITE}").strip()

        print("\nUSERNAME OSINT")
        print(username_osint(username))

        return

    print(f"{RED}Invalid option{WHITE}")
