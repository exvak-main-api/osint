import requests
import re


def get_title(domain):
    try:
        urls = [f"https://{domain}", f"http://{domain}"]

        for url in urls:
            try:
                r = requests.get(url, timeout=5, headers={
                    "User-Agent": "Mozilla/5.0"
                })

                match = re.search(r"<title>(.*?)</title>", r.text, re.IGNORECASE | re.DOTALL)
                if match:
                    return match.group(1).strip()

                return None

            except Exception:
                continue

        return None

    except Exception:
        return None


def get_headers(domain):
    try:
        r = requests.get(f"https://{domain}", timeout=5, headers={
            "User-Agent": "Mozilla/5.0"
        })

        return dict(r.headers)

    except Exception:
        return {}
