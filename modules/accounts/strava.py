from lib.requests import Request

async def strava(target: str):

    try:
        req = await Request(
            "https://www.strava.com/frontend/athletes/email_unique",
            params={'email': target}
        ).get()

        text = req.text.lower()

        if "false" in text:
            return True

        return False

    except:
        return False
