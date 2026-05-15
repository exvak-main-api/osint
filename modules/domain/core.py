from modules.domain.whois import get_whois
from modules.domain.dns import get_dns
from modules.domain.email_patterns import guess_patterns
from modules.domain.website import get_title

def domain_info(domain):
    return {
        "whois": get_whois(domain),
        "dns": get_dns(domain),
        "email_patterns": guess_patterns(domain),
        "title": get_title(domain)
    }
