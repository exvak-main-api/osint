from lib.requests import Request

async def chess(target: str):

    try:
        r = await Request(
            f"https://www.chess.com/callback/email/available?email={target}"
        ).post()

        try:
            data = r.json()
        except:
            return False

        if data.get('isEmailAvailable') == False:
            return True

        return False

    except:
        return False
