from lib.requests import Request

async def twitter(target: str):

    try:
        r = await Request(
            f"https://api.twitter.com/i/users/email_available.json?email={target}"
        ).get()

        try:
            data = r.json()
        except:
            return False

        if data.get("taken") is True:
            return True

        return False

    except:
        return False
