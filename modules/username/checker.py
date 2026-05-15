import requests
from .sites import SITES
from .headers import get_headers


def is_valid_response(text):
    t = text.lower()

    bad_signals = [
        "not found",
        "page not found",
        "couldn't find",
        "doesn't exist",
        "user not found",
        "404",
        "error 404"
    ]

    return not any(b in t for b in bad_signals)


def check_site(name, url, username):
    try:
        target = url.format(username)
        r = requests.get(target, headers=get_headers(), timeout=7)

        if r.status_code != 200:
            return False, None

        if not is_valid_response(r.text):
            return False, None

        return True, target

    except:
        return False, None


def username_osint(username):
    results = {}

    for name, url in SITES.items():
        found, link = check_site(name, url, username)

        results[name] = {
            "found": found,
            "url": link
        }

    return results
