async def parser():
    await Version_Checker.checker()

    print(f"""
{GREEN}
=====================================
        EXVAK OSINT PANEL
=====================================
{WHITE}
""")

    print(f"{YELLOW}[1]{WHITE} Email OSINT Search")
    print(f"{YELLOW}[0]{WHITE} Exit\n")

    choice = input(f"{YELLOW}Select option > {WHITE}").strip()

    if choice == "0":
        print(f"{RED}Exiting...{WHITE}")
        return

    if choice != "1":
        print(f"{RED}Invalid option{WHITE}")
        return

    target = input(f"\n{YELLOW}Enter email > {WHITE}").strip()

    EMAIL_REGEX = r'[a-zA-Z0-9._+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'

    if not re.match(EMAIL_REGEX, target):
        print(f"{RED}>{WHITE} The target isn't an email.")
        return

    print(f"\n🔎 Currently researching on: '{RED}{target}{WHITE}' {YELLOW}...\n")

    print(f"\n{PURPLE}📁 Leak search{YELLOW}...\n")

    try:
        await Pastebin_Dumper(target).paste_check()
    except:
        print(f"{RED}Pastebin error{WHITE}")

    print()

    try:
        await Cavalier(target).loader()
    except:
        print(f"{RED}HudsonRock error{WHITE}")

    print(f"\n{GREEN}🎭 Account search{YELLOW}...\n")

    modules = [
        adobe, bandlab, chess, duolingo, flickr,
        github, gravatar, instagram, pinterest,
        protonmail, spotify, strava, x
    ]

    for m in modules:
        try:
            await m(target)
        except:
            print(f"{RED}{m.__name__} failed{WHITE}")

    try:
        imgur(target)
    except:
        pass

    try:
        pornhub(target)
    except:
        pass

    print(f"\n{PINK}📧 Email generation{WHITE}\n")

    try:
        Email_Gen(target).printer()
    except:
        print(f"{RED}Email gen error{WHITE}")
