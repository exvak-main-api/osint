import requests
import re
import socket
from urllib.parse import urlparse


def resolve_ip(domain):
    try:
        return socket.gethostbyname(domain)
    except:
        return None


def fetch_html(domain):
    try:
        r = requests.get(
            f"http://{domain}",
            timeout=8,
            headers={
                "User-Agent": "Mozilla/5.0",
                "Accept": "text/html"
            }
        )
        return r.text, r.status_code, str(r.headers)
    except:
        return None, None, None


def extract_title(html):
    try:
        m = re.search(r"<title>(.*?)</title>", html, re.IGNORECASE | re.DOTALL)
        return m.group(1).strip() if m else None
    except:
        return None


def detect_technologies(html, headers_text):
    tech = []

    if not html:
        return tech

    h = html.lower()
    hdrs = headers_text.lower() if headers_text else ""

    if "wordpress" in h:
        tech.append("WordPress")
    if "wp-content" in h:
        tech.append("WordPress CMS")

    if "react" in h or "reactroot" in h:
        tech.append("React")

    if "vue" in h:
        tech.append("Vue.js")

    if "angular" in h:
        tech.append("Angular")

    if "cloudflare" in hdrs:
        tech.append("Cloudflare")

    if "nginx" in hdrs:
        tech.append("Nginx")

    if "apache" in hdrs:
        tech.append("Apache")

    if "next.js" in h or "__next" in h:
        tech.append("Next.js")

    return list(set(tech))


def detect_security_headers(headers_text):
    headers_text = (headers_text or "").lower()

    security = {
        "https": False,
        "hsts": False,
        "csp": False,
        "xframe": False
    }

    if "strict-transport-security" in headers_text:
        security["hsts"] = True
    if "content-security-policy" in headers_text:
        security["csp"] = True
    if "x-frame-options" in headers_text:
        security["xframe"] = True
    if "https" in headers_text:
        security["https"] = True

    return security


def website_info(domain):
    try:
        ip = resolve_ip(domain)
        html, status, headers = fetch_html(domain)

        title = extract_title(html) if html else None
        tech = detect_technologies(html, headers)
        security = detect_security_headers(headers)

        return {
            "domain": domain,
            "ip": ip,
            "status_code": status,
            "title": title,
            "technologies": tech,
            "security_headers": security,
            "length": len(html) if html else 0,
        }

    except:
        return {
            "domain": domain,
            "error": True
        }
