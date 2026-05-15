import re
import asyncio
from lib.colors import *
from lib.update import Version_Checker
from lib.emails_gen import Email_Gen
from modules import *
from modules.domain import domain_info, ip_asn_info
from modules.domain.correlation import correlate
from modules.domain.enrichment import crt_subdomains, validate_subdomains, reverse_ip_lookup
from modules.username import username_osint


EMAIL_REGEX = re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}')


def print_section(title):
    print(f"\n{GREEN}{title}{WHITE}\n")


async def parser():

    try:
        await Version_Checker().checker()
    except:
        print(f"{RED}[!] Version check failed{WHITE}")

    print(f"""
{GREEN}
=====================================
        EXVAK OSINT PANEL
=====================================
{WHITE}
""")

    print(f"{YELLOW}[1]{WHITE} Email OSINT Search")
    print(f"{YELLOW}[2]{WHITE} Phone OSINT Search")
    print(f"{YELLOW}[3]{WHITE} Domain OSINT Search")
    print(f"{YELLOW}[4]{WHITE} Username OSINT Search")
    print(f"{YELLOW}[0]{WHITE} Exit\n")

    choice = input(f"{YELLOW}Select option > {WHITE}").strip()

    if choice == "0":
        print(f"{RED}Exiting...{WHITE}")
        return

    if choice == "1":

        target = input(f"\n{YELLOW}Enter email > {WHITE}").strip()

        if not EMAIL_REGEX.match(target):
            print(f"{RED}>{WHITE} Invalid email")
            return

        print(f"\n🔎 Researching: '{RED}{target}{WHITE}' {YELLOW}...\n")

        print_section("Leak search")

        try:
            await Pastebin_Dumper(target).paste_check()
        except:
            print(f"{RED}Pastebin error{WHITE}")

        try:
            await Cavalier(target).loader()
        except:
            print(f"{RED}HudsonRock error{WHITE}")

        print_section("Account search")

        modules = [
            ("adobe", adobe), ("bandlab", bandlab), ("chess", chess),
            ("duolingo", duolingo), ("flickr", flickr), ("github", github),
            ("gravatar", gravatar), ("instagram", instagram),
            ("pinterest", pinterest), ("protonmail", protonmail),
            ("spotify", spotify), ("strava", strava), ("twitter", twitter)
        ]

        for name, func in modules:
            try:
                result = await func(target)

                if isinstance(result, tuple):
                    found, data = result
                else:
                    found, data = bool(result), None

                print(f"{name} - {'found' if found else 'not found'}")

                if data:
                    print(f"   └── {data}")

            except:
                print(f"{name} - error")

        try:
            imgur(target)
        except:
            pass

        try:
            pornhub(target)
        except:
            pass

        try:
            Email_Gen(target).printer()
        except:
            print(f"{RED}Email gen error{WHITE}")

        return

    if choice == "2":

        target = input(f"\n{YELLOW}Enter phone (+country code) > {WHITE}").strip()

        print(f"\n🔎 Researching: '{RED}{target}{WHITE}' {YELLOW}...\n")

        try:
            from modules.phone.lookup import lookup

            result = await lookup(target)

            if isinstance(result, tuple):
                found, data = result
            else:
                found, data = bool(result), None

            print(f"phone - {'found' if found else 'not found'}")

            if data:
                print(f"   └── {data}")

        except:
            print(f"{RED}phone error{WHITE}")

        return

    if choice == "3":

        target = input(f"\n{YELLOW}Enter domain > {WHITE}").strip()

        if "." not in target:
            print(f"{RED}>{WHITE} Invalid domain")
            return

        print(f"\n🔎 Analyzing: '{RED}{target}{WHITE}' {YELLOW}...\n")

        data = None
        ip_data = None

        try:
            data = domain_info(target)
        except:
            print(f"{RED}domain error{WHITE}")

        try:
            ip_data = ip_asn_info(target)
        except:
            print(f"{RED}ip/asn error{WHITE}")

        if data:

            print_section("WHOIS")
            print(data.get("whois"))

            print_section("DNS")
            print(data.get("dns"))

            print_section("EMAIL PATTERNS")
            print(data.get("email_patterns"))

            print_section("WEBSITE")
            print(data.get("title"))

        if ip_data:

            print_section("IP + ASN")

            for k, v in ip_data.items():
                print(f"{k}: {v}")

        print_section("SUBDOMAIN DISCOVERY")

        try:
            subs = crt_subdomains(target)
            real_subs = validate_subdomains(subs)

            for s in real_subs:
                print(f"- {s}")
        except:
            print(f"{RED}subdomain error{WHITE}")

        print_section("REVERSE IP LOOKUP")

        try:
            rev = reverse_ip_lookup(target)

            print(f"IP: {rev.get('ip')}")

            for d in rev.get("domains", []):
                print(f"- {d}")
        except:
            print(f"{RED}reverse ip error{WHITE}")

        if data and ip_data:

            try:
                corr = correlate(
                    target,
                    data.get("whois", {}),
                    data.get("dns", {}),
                    ip_data
                )

                print_section("CORRELATION ENGINE")

                print(f"Risk Score: {corr['risk_score']}/100")

                for s in corr["signals"]:
                    print(f"- {s}")

            except:
                print(f"{RED}correlation error{WHITE}")

        return

    if choice == "4":

        target = input(f"\n{YELLOW}Enter username > {WHITE}").strip()

        print(f"\n🔎 Searching username: '{RED}{target}{WHITE}' {YELLOW}...\n")

        try:
            results = username_osint(target)

            for site, data in results.items():

                found = data.get("found")
                url = data.get("url")

                print(f"{site} - {'found' if found else 'not found'}")

                if url:
                    print(f"   └── {url}")

        except:
            print(f"{RED}username osint error{WHITE}")

        return

    print(f"{RED}Invalid option{WHITE}")
