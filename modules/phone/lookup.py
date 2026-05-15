import re
import asyncio
import phonenumbers as p

from phonenumbers import (
    PhoneNumberType,
    carrier,
    geocoder,
    number_type,
    timezone,
)

_NUMBER_TYPE_LABELS = {
    PhoneNumberType.MOBILE: "Mobile",
    PhoneNumberType.FIXED_LINE: "Fixed Line",
    PhoneNumberType.FIXED_LINE_OR_MOBILE: "Fixed Line or Mobile",
    PhoneNumberType.TOLL_FREE: "Toll-Free",
    PhoneNumberType.PREMIUM_RATE: "Premium Rate",
    PhoneNumberType.SHARED_COST: "Shared Cost",
    PhoneNumberType.VOIP: "VoIP",
    PhoneNumberType.PERSONAL_NUMBER: "Personal Number",
    PhoneNumberType.PAGER: "Pager",
    PhoneNumberType.UAN: "UAN",
    PhoneNumberType.VOICEMAIL: "Voicemail",
    PhoneNumberType.UNKNOWN: "Unknown",
}


async def lookup(phone_number: str) -> bool:
    phone_number = phone_number.strip()

    try:
        ph_no = p.parse(phone_number)
    except p.NumberParseException:
        print("[!] Invalid phone number format")
        return False

    if not p.is_valid_number(ph_no):
        print("[!] Warning: number may be invalid")

    await _print_number_info(ph_no)
    return await _run_ignorant(ph_no)


async def _print_number_info(ph_no: p.PhoneNumber):
    e164 = p.format_number(ph_no, p.PhoneNumberFormat.E164)
    intl = p.format_number(ph_no, p.PhoneNumberFormat.INTERNATIONAL)
    national = p.format_number(ph_no, p.PhoneNumberFormat.NATIONAL)

    country = p.region_code_for_country_code(ph_no.country_code or 0)
    carrier_name = carrier.name_for_number(ph_no, "en")
    time_zones = timezone.time_zones_for_number(ph_no)
    region = geocoder.description_for_number(ph_no, "en")
    n_type = _NUMBER_TYPE_LABELS.get(int(number_type(ph_no)), "Unknown")

    print(f"\n[+] Looking up {intl}...\n")
    await asyncio.sleep(0.3)

    print("=== Phone Number Details ===")
    print(f"E.164 Format  : {e164}")
    print(f"International : {intl}")
    print(f"National      : {national}")
    print(f"Country Code  : +{ph_no.country_code}")
    print(f"Country       : {country or 'Unknown'}")
    print(f"Region        : {region or 'Unknown'}")
    print(f"Type          : {n_type}")
    print(f"Carrier       : {carrier_name or 'Unknown'}")
    print(f"Time Zones    : {', '.join(time_zones) if time_zones else 'Unknown'}")


async def _run_ignorant(ph_no: p.PhoneNumber) -> bool:
    print("\n=== Social Media Presence ===\n")

    country_code_arg = f"+{ph_no.country_code}"
    national_number_arg = str(ph_no.national_number)

    try:
        proc = await asyncio.create_subprocess_exec(
            "ignorant",
            "--only-used",
            "--no-color",
            "--no-clear",
            country_code_arg,
            national_number_arg,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )

        stdout, stderr = await proc.communicate()
        output = (stdout.decode() + stderr.decode()).strip()

        if not output:
            print("[!] No output from tool")
            return False

        found = _parse_ignorant_output(output)

        if not found:
            print("[!] No platforms found")
            return False

        print(f"[+] Found on {len(found)} platform(s):")
        for site in found:
            print(f"    - {site}")

        return True

    except FileNotFoundError:
        print("[!] ignorant not installed")
        return False
    except Exception as exc:
        print(f"[!] Error: {exc}")
        return False


def _parse_ignorant_output(output: str) -> list[str]:
    ansi_re = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")
    found = []

    for line in output.splitlines():
        clean = ansi_re.sub("", line).strip()

        match = re.match(r"^\[(\+)\]\s*(\S+)", clean)
        if match:
            domain = match.group(2)
            if "." in domain:
                found.append(domain)

    return sorted(found)
