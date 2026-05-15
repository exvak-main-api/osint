from lib.requests import Request

async def duolingo(target: str):

    try:
        r = await Request(
            "https://www.duolingo.com/2017-06-30/users",
            params={'email': target}
        ).get()

        if '{"users":[]}' in r.text:
            return False

        try:
            data = r.json()

            if data.get('users') and len(data['users']) > 0:
                return True

            return False

        except:
            return False

    except:
        return False
