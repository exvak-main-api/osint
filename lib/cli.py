import re
import asyncio
from lib.colors import *
from lib.update import Version_Checker
from lib.emails_gen import Email_Gen
from modules import *

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
    print(f"{YELLOW}[3]{WHITE} Instagram OSINT Search")
    print(f"{YELLOW}[0]{WHITE} Exit\n")

    choice = input(f"{YELLOW}Select option > {WHITE}").strip()

    if choice == "0":
        print(f"{RED}Exiting...{WHITE}")
        return

    if choice == "1":

        target = input(f"\n{YELLOW}Enter email > {WHITE}").strip()

        EMAIL_REGEX = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'

        if not re.match(EMAIL_REGEX, target):
            print(f"{RED}>{WHITE} The target isn't an email.")
            return

        print(f"\n🔎 Researching: '{RED}{target}{WHITE}' {YELLOW}...\n")
        print(f"\n{PURPLE}📁 Leak search{YELLOW}...\n")

        try:
            await Pastebin_Dumper(target).paste_check()
        except:
            print(f"{RED}Pastebin error{WHITE}")

        try:
            await Cavalier(target).loader()
        except:
            print(f"{RED}HudsonRock error{WHITE}")

        print(f"\n{GREEN}🎭 Account search{YELLOW}...\n")

        modules = [
            ("adobe", adobe),
            ("bandlab", bandlab),
            ("chess", chess),
            ("duolingo", duolingo),
            ("flickr", flickr),
            ("github", github),
            ("gravatar", gravatar),
            ("instagram", instagram),
            ("pinterest", pinterest),
            ("protonmail", protonmail),
            ("spotify", spotify),
            ("strava", strava),
            ("twitter", twitter)
        ]

        for name, func in modules:
            try:
                result = await func(target)

                if isinstance(result, tuple):
                    found, data = result
                else:
                    found, data = bool(result), None

                if found:
                    print(f"{name} - found")
                    if data:
                        print(f"   └── {data}")
                else:
                    print(f"{name} - not found")

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

        target = input(f"\n{YELLOW}Enter phone number (+country code) > {WHITE}").strip()

        print(f"\n🔎 Researching: '{RED}{target}{WHITE}' {YELLOW}...\n")

        try:
            from modules.phone.lookup import lookup

            result = await lookup(target)

            if isinstance(result, tuple):
                found, data = result
            else:
                found, data = bool(result), None

            if found:
                print("phone - found")
                if data:
                    print(f"   └── {data}")
            else:
                print("phone - not found")

        except:
            print("phone - error")

        return

    print(f"{RED}Invalid option{WHITE}")
