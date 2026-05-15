from lib.requests import Request
from datetime import datetime
import re

Session = Request(url=None).Session()

async def generate_auth_cookie():
    url_session = "https://account.proton.me/api/auth/v4/sessions"
    url_cookies = "https://account.proton.me/api/core/v4/auth/cookies"

    data_session = {
        "x-pm-appversion": "web-account@5.0.153.3",
        "x-pm-locale": "en_US",
        "x-enforce-unauthsession": "true"
    }

    response = Session.post(url_session, headers=data_session)

    json_dump = response.json()

    access_token = json_dump.get('AccessToken')
    refresh_token = json_dump.get('RefreshToken')
    uid = json_dump.get('UID')

    if not all([access_token, refresh_token, uid]):
        return None, None

    data_cookie = {
        "x-pm-appversion": "web-account@5.0.153.3",
        "x-pm-locale": "en_US",
        "x-pm-uid": uid,
        "Authorization": f"Bearer {access_token}"
    }

    request_data = {
        "GrantType": "refresh_token",
        "Persistent": 0,
        "RedirectURI": "https://protonmail.com",
        "RefreshToken": refresh_token,
        "ResponseType": "token",
        "State": "C72g4sTNltu4TAL5bUQlnvUT",
        "UID": uid
    }

    response = Session.post(url_cookies, headers=data_cookie, json=request_data)

    auth_cookie = None
    for cookie in response.cookies:
        if "AUTH" in str(cookie):
            auth_cookie = str(cookie).split(" ")[1]
            break

    return uid, auth_cookie


async def protonmail(target: str):

    try:
        domain = target.split("@")[1]

        if domain not in [
            "pm.me",
            "proton.me",
            "protonmail.com",
            "protonmail.ch"
        ]:
            return False

        uid, auth_cookie = await generate_auth_cookie()

        if not uid or not auth_cookie:
            return False

        headers = {
            "x-pm-appversion": "web-account@5.0.153.3",
            "x-pm-locale": "en_US",
            "x-pm-uid": uid,
            "Cookie": auth_cookie
        }

        params = {
            "Name": target,
            "ParseDomain": "1"
        }

        r = Session.get(
            "https://account.proton.me/api/core/v4/users/available",
            headers=headers,
            params=params
        )

        text = r.text

        if '"Suggestions":[]' in text:
            return False

        if '"Code":1000' in text:
            return False

        # account exists / found scenario
        try:
            api = await Request(
                f"https://api.protonmail.ch/pks/lookup?op=index&search={target}"
            ).get()

            match = re.search(r'\b\d{10}\b', api.text)

            if match:
                timestamp = int(match.group())
                datetime.fromtimestamp(timestamp)

        except:
            pass

        return True

    except:
        return False
