EXVAK OSINT PANEL

Advanced modular OSINT framework for email, username, domain, infrastructure, and anomaly intelligence.


---

Features

Email Intelligence

Email pattern generation

Role account discovery

Organization naming style detection

Domain-linked email intelligence


Username OSINT

Multi-site username enumeration

Real profile detection

URL extraction

Large platform support


Domain Intelligence

WHOIS analysis

Domain age detection

Expiration analysis

Registrar profiling

Privacy protection detection


DNS Intelligence

A / AAAA records

MX records

TXT records

SPF detection

DMARC detection

NS analysis

SOA / SRV support


IP + ASN Intelligence

ASN detection

Hosting provider analysis

Infrastructure fingerprinting

Geolocation

Cloud provider detection

Network intelligence


Website Intelligence

Website title extraction

HTTP fingerprinting

Technology detection

CMS detection

Framework detection

Security header analysis


Subdomain Intelligence

Passive subdomain discovery

Real subdomain validation

IP resolution

Asset enrichment


Reverse IP Lookup

Shared hosting detection

Related domain discovery

Infrastructure clustering


Correlation Engine

Risk scoring

Infrastructure analysis

Domain maturity analysis

Email security analysis

Threat indicators


Smart Anomaly Detection

Infrastructure inconsistencies

DNS abnormalities

Cloud deployment anomalies

Email security gaps

Minimal footprint detection


Graph Intelligence

Entity relationship mapping

Domain → IP linking

Domain → Subdomain linking

Nameserver mapping


Reporting System

Unified intelligence reports

JSON report export

Structured intelligence output



---

Project Structure

osint-main/
│
├── main.py
├── requirements.txt
│
├── lib/
│   ├── cli.py
│   ├── colors.py
│   ├── update.py
│   └── emails_gen.py
│
├── modules/
│   ├── __init__.py
│   │
│   ├── engine.py
│   ├── graph.py
│   ├── report.py
│   ├── scoring.py
│   ├── subdomains.py
│   │
│   ├── username/
│   │   ├── __init__.py
│   │   ├── checker.py
│   │   ├── headers.py
│   │   ├── helpers.py
│   │   ├── sites.py
│   │   └── useragents.py
│   │
│   └── domain/
│       ├── __init__.py
│       ├── whois.py
│       ├── dns.py
│       ├── ip_asn.py
│       ├── website.py
│       ├── enrichment.py
│       ├── correlation.py
│       ├── anomaly.py
│       └── email_patterns.py


---

Installation

Clone

git clone https://github.com/exvak-main-api/osint
cd osint

Install Requirements

pip install -r requirements.txt

Run

python main.py


---

Requirements

requests
dnspython
python-whois
aiohttp
beautifulsoup4
lxml


---

CLI Preview

=====================================
        EXVAK OSINT PANEL
=====================================

[1] Email OSINT
[2] Phone OSINT
[3] Domain OSINT
[4] Username OSINT
[0] Exit


---

Example Domain Scan

DOMAIN: google.com

WHOIS
- Registrar
- Creation date
- Expiration
- Privacy

DNS
- MX
- SPF
- DMARC
- NS

IP / ASN
- Google LLC
- ASN
- Geo

CORRELATION
- Risk Score
- Infrastructure signals

ANOMALY
- Email security posture
- Infrastructure consistency


---

Supported Intelligence Types

Type	Supported

Email Intelligence	Yes
Username Intelligence	Yes
Domain Intelligence	Yes
DNS Analysis	Yes
Infrastructure Analysis	Yes
ASN Intelligence	Yes
Website Fingerprinting	Yes
Subdomain Discovery	Yes
Reverse IP Lookup	Yes
Correlation Engine	Yes
Anomaly Detection	Yes
Graph Intelligence	Yes
Report Export	Yes



---

Engine Capabilities

Passive OSINT

DNS collection

WHOIS collection

Public infrastructure mapping

Username enumeration


Infrastructure Intelligence

Hosting analysis

CDN detection

Cloud infrastructure mapping

ASN intelligence


Threat Analysis

Risk scoring

Domain maturity analysis

Security posture analysis

Infrastructure anomaly detection


Relationship Mapping

Entity graph generation

Asset linking

Infrastructure correlation



---

Output

The framework generates:

Structured intelligence output

Risk scoring

Anomaly scoring

Relationship graphs

Exportable JSON reports



---

Notes

Passive OSINT focused

Modular architecture

Easily extensible

CLI optimized

Designed for investigations and infrastructure analysis



---

License

MIT License


---

Author

EXVAK Intelligence Framework
