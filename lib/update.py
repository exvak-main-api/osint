import json
from .requests import Request
from .colors import *

class Version_Checker:
    async def checker(self):
        with open('config.json', "+r", encoding='utf-8') as file:
            reader = json.loads(file.read())

        version = reader['version']['number']
        name = reader['version']['name']

        print(f"[ {RED}{name} version{WHITE} ]")

        r = await Request("https://raw.githubusercontent.com/exvak-main-api/osint/refs/heads/main/config.json").get()
        
        conf = json.loads(r.text)

        current_version = conf['version']['number']

        if version == current_version:
            print(f"\n{GREEN}>{WHITE} 🎊 You're up to date ! ~ v{current_version}\n")

        else: 
            print(f"\n{RED}>{WHITE} 🔥 The new version {current_version} is available\n")
