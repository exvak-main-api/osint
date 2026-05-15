import re
import asyncio
from lib.colors import *
from lib.update import Version_Checker
from lib.emails_gen import Email_Gen
from modules import *
from modules.domain import domain_info, ip_asn_info


EMAIL_REGEX = re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}')


def print_section(title):
    print(f"\n{GREEN}{title}{WHITE}\n")


def safe_call(func, *args, error_msg="error", is_async=False):
    try:
        if is_async:
            return asyncio.run(func(*args))
        return func(*args)
    except:
        print(f"{RED}{error_msg}{WHITE}")
        return None


async def parser():

    safe_call(Version_Checker().checker, is_async=True)

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
    print(f"{YELLOW}[0]{WHITE} Exit\n")

    choice = input(f"{YELLOW}Select option > {WHITE}").strip()

    if choice == "0":
        print(f"{RED}Exiting...{WHITE}")
        return

    # ================= EMAIL =================
    if choice == "1":

        target = input(f"\n{YELLOW}Enter email > {WHITE}").strip()

        if not EMAIL_REGEX.match(target):
            print(f"{RED}>{WHITE} Invalid email.")
            return

        print(f"\n🔎 Researching: '{RED}{target}{WHITE}' {YELLOW}...\n")

        print_section("Leak search")

        safe_call(Pastebin_Dumper(target).paste_check, error_msg="Pastebin error", is_async=True)
        safe_call(Cavalier(target).loader, error_msg="HudsonRock error", is_async=True)

        print_section("Account search")

        modules = [
            ("adobe", adobe), ("bandlab", bandlab), ("chess", chess),
            ("duolingo", duolingo), ("flickr", flickr), ("github", github),
            ("gravatar", gravatar), ("instagram", instagram),
            ("pinterest", pinterest), ("protonmail", protonmail),
            ("spotify", spotify), ("strava", strava), ("twitter", twitter)
        ]

        for name, func in modules:
            result = safe_call(func, target, error_msg=f"{name} error", is_async=True)

            if isinstance(result, tuple):
                found, data = result
            else:
                found, data = bool(result), None

            print(f"{name} - {'found' if found else 'not found'}")
            if data:
                print(f"   └── {data}")

        safe_call(imgur, target)
        safe_call(pornhub, target)
        safe_call(lambda: Email_Gen(target).printer())

        return

    # ================= PHONE =================
    if choice == "2":

        target = input(f"\n{YELLOW}Enter phone (+country code) > {WHITE}").strip()

        print(f"\n🔎 Researching: '{RED}{target}{WHITE}' {YELLOW}...\n")

        from modules.phone.lookup import lookup

        result = safe_call(lookup, target, error_msg="phone error", is_async=True)

        if isinstance(result, tuple):
            found, data = result
        else:
            found, data = bool(result), None

        print(f"phone - {'found' if found else 'not found'}")
        if data:
            print(f"   └── {data}")

        return

    # ================= DOMAIN =================
    if choice == "3":

        target = input(f"\n{YELLOW}Enter domain > {WHITE}").strip()

        if "." not in target:
            print(f"{RED}>{WHITE} Invalid domain.")
            return

        print(f"\n🔎 Analyzing: '{RED}{target}{WHITE}' {YELLOW}...\n")

        data = safe_call(domain_info, target, error_msg="domain error")

        if data:
            print_section("WHOIS")
            print(data.get("whois"))

            print_section("DNS")
            print(data.get("dns"))

            print_section("EMAIL PATTERNS")
            print(data.get("email_patterns"))

            print_section("WEBSITE")
            print(data.get("title"))

        ip_data = safe_call(ip_asn_info, target, error_msg="ip/asn error")

        if ip_data:
            print_section("IP + ASN")
            for k, v in ip_data.items():
                print(f"{k}: {v}")

        return

    print(f"{RED}Invalid option{WHITE}")
