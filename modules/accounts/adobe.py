from lib.requests import *

async def adobe(target: str):
    try:
        data = {
            "username": target,
            "usernameType": "EMAIL"
        }

        headers = {
            'x-ims-clientid': 'homepage_milo',
            'content-type': 'application/json'
        }

        r = await Request(
            "https://auth.services.adobe.com/signin/v2/users/accounts",
            headers=headers,
            json=data
        ).post()

        try:
            data = r.json()

            if isinstance(data, list) and len(data) > 0:
                if data[0].get("authenticationMethods"):
                    return True

            return False

        except:
            return False

    except:
        return False
