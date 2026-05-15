from lib.requests import Request

async def pinterest(target: str):

    try:
        params = {
            "source_url": "/",
            "data": '{"options": {"email": "' + target + '"}, "context": {}}'
        }

        r = await Request(
            "https://www.pinterest.fr/resource/EmailExistsResource/get/",
            params=params
        ).get()

        try:
            data = r.json()
        except:
            return False

        if (
            data.get("resource_response")
            and data["resource_response"].get("data")
        ):
            return True

        return False

    except:
        return False
