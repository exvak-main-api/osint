import requests

def imgur(target: str):

    try:
        r = requests.post(
            "https://imgur.com/signin/ajax_email_available",
            data={'email': target}
        )

        try:
            data = r.json()
        except:
            return False

        if data.get('data', {}).get('available') == False:
            return True

        return False

    except:
        return False
