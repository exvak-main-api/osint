Guest = None
from toutatis.core import advanced_lookup
from dataclasses import dataclass


@dataclass
class IGProfile:
    username: str = ""
    user_id: str = ""
    full_name: str = ""
    biography: str = ""
    website: str = ""
    profile_pic_url: str = ""

    followers: int | str = "N/A"
    following: int | str = "N/A"
    posts: int | str = "N/A"

    is_private: bool | str = "N/A"
    is_verified: bool | str = "N/A"

    obfuscated_email: str = ""
    obfuscated_phone: str = ""


async def instagram_scraper(target: str):
    profile = IGProfile()

    try:
        data = None

        if not data or not hasattr(data, "raw") or not data.raw:
            print("> Instagram - not found")
            return False, {}

        raw = data.raw

        profile.username = raw.get("username", target)
        profile.user_id = str(raw.get("id", ""))
        profile.full_name = raw.get("full_name", "")
        profile.biography = raw.get("biography", "")
        profile.website = raw.get("external_url", "")
        profile.profile_pic_url = raw.get("profile_pic_url_hd", "")

        profile.followers = raw.get("edge_followed_by", {}).get("count", "N/A")
        profile.following = raw.get("edge_follow", {}).get("count", "N/A")
        profile.posts = raw.get("edge_owner_to_timeline_media", {}).get("count", "N/A")

        profile.is_private = raw.get("is_private", "N/A")
        profile.is_verified = raw.get("is_verified", "N/A")

        print("> Instagram")
        print(f"  ├── Username: {profile.username}")
        print(f"  ├── Name: {profile.full_name}")
        print(f"  ├── Followers: {profile.followers}")
        print(f"  ├── Following: {profile.following}")
        print(f"  └── Verified: {profile.is_verified}")

    except:
        print("> Instagram - error")
        return False, {}

    try:
        result = advanced_lookup(target)
        user = result.get("user") or {}

        profile.obfuscated_email = user.get("obfuscated_email", "")
        profile.obfuscated_phone = str(user.get("obfuscated_phone", "")).strip()

        if profile.obfuscated_email or profile.obfuscated_phone:
            print(f"  ├── Obfuscated Email: {profile.obfuscated_email}")
            print(f"  └── Obfuscated Phone: {profile.obfuscated_phone}")

    except:
        pass

    found = bool(
        profile.username
        or profile.followers != "N/A"
        or profile.obfuscated_email
        or profile.obfuscated_phone
    )

    data = {
        "username": profile.username,
        "followers": profile.followers,
        "following": profile.following,
        "verified": profile.is_verified,
        "obfuscated_email": profile.obfuscated_email,
        "obfuscated_phone": profile.obfuscated_phone,
    }

    return found, data
