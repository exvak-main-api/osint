from lib.requests import Request
from datetime import datetime

async def github(target: str):

    try:
        r = await Request(
            f"https://api.github.com/search/users?q={target}+in:email"
        ).get()

        try:
            data = r.json()
        except:
            return False

        if data.get("total_count", 0) == 0:
            return False

        if not data.get("items"):
            return False

        user = data["items"][0]

        try:
            api = await Request(
                f"https://api.github.com/users/{user['login']}"
            ).get()

            profile = api.json()

            creation = profile.get('created_at')
            update = profile.get('updated_at')

            if creation:
                c_datetime = datetime.fromisoformat(
                    creation.replace("Z", "+00:00")
                )
                c_date = c_datetime.strftime("%Y-%m-%d %H:%M:%S")

                print(f"  ├── Username : {user['login']}")
                print(f"  ├── Created : {c_date}")

            if update:
                u_datetime = datetime.fromisoformat(
                    update.replace("Z", "+00:00")
                )
                u_date = u_datetime.strftime("%Y-%m-%d %H:%M:%S")

                print(f"  ├── Updated : {u_date}")

            if profile.get('name'):
                print(f"  ├── Name : {profile['name']}")

            print(f"  ├── Id : {user['id']}")
            print(f"  ├── Avatar : {user['avatar_url']}")
            print(f"  └── Account : https://github.com/{user['login']}/")

        except:
            pass

        return True

    except:
        return False
