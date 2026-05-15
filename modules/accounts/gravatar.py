from lib.requests import Request
import hashlib

async def gravatar(target: str):

    try:
        encoded_email = target.lower().encode('utf-8')
        hashed_email = hashlib.sha256(encoded_email).hexdigest()

        r = await Request(
            f"https://en.gravatar.com/{hashed_email}.json"
        ).get()

        if "User not found" in r.text:
            return False

        try:
            data = r.json()['entry'][0]

            print(f"  ├── Username : {data['displayName']}")

            try:
                avatar_url = str(data['thumbnailUrl']).replace("\\", "")
                print(f"  ├── Avatar : {avatar_url}")
            except:
                pass

            print(
                f"  └── Account : https://gravatar.com/{data['displayName']}/"
            )

            return True

        except:
            return False

    except:
        return False
