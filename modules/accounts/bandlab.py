from lib.requests import Request

async def bandlab(target: str):

    try:
        r = await Request(
            "https://www.bandlab.com/api/v1.3/validation/user",
            params={'email': target}
        ).get()

        try:
            data = r.json()
        except:
            return False

        if data.get('isValid'):
            if data.get('isAvailable') == False:
                return True

        return False

    except:
        return False
