from bs4 import BeautifulSoup
from lib.requests import Request

def pornhub(target: str):

    try:
        s = Request(url=None).Session()

        r = s.get("https://fr.pornhub.com/signup")

        soup = BeautifulSoup(r.text, "html.parser")

        token_tag = soup.find(attrs={"name": "token"})
        if not token_tag:
            return False

        token = token_tag.get("value")

        params = {"token": token}
        data = {
            "check_what": "email",
            "email": target
        }

        api = s.post(
            "https://fr.pornhub.com/user/create_account_check",
            params=params,
            data=data
        )

        try:
            resp = api.json()
        except:
            s.close()
            return False

        s.close()

        if resp.get("email") == "create_account_failed":
            return True

        return False

    except:
        try:
            s.close()
        except:
            pass
        return False
