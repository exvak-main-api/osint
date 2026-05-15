from lib.requests import Request

async def spotify(target: str):

    try:
        r = await Request(
            f"https://spclient.wg.spotify.com/signup/public/v1/account?validate=1&email={target}"
        ).get()

        try:
            data = r.json()
        except:
            return False

        if data.get("status") == 20:
            return True

        return False

    except:
        return False
