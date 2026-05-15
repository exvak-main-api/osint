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
        result = advanced_lookup(target) or {}
        user = result.get("user") or {}

        if not user or user.get("message") == "No users found":
            print("> Instagram - not found")
            return False, {}

        profile.username = user.get("username", target)
        profile.user_id = str(user.get("userID", user.get("pk", "")))
        profile.full_name = user.get("full_name", "")
        profile.biography = user.get("biography", "")
        profile.website = user.get("external_url", "")
        profile.profile_pic_url = user.get("profile_pic_url", "")

        profile.followers = user.get("follower_count", "N/A")
        profile.following = user.get("following_count", "N/A")
        profile.posts = user.get("media_count", "N/A")

        profile.is_private = user.get("is_private", "N/A")
        profile.is_verified = user.get("is_verified", "N/A")

        print("> Instagram")
        print(f"  ├── Username: {profile.username}")
        print(f"  ├── Name: {profile.full_name}")
        print(f"  ├── Followers: {profile.followers}")
        print(f"  ├── Following: {profile.following}")
        print(f"  └── Verified: {profile.is_verified}")

        obf_email = user.get("obfuscated_email", "")
        obf_phone = str(user.get("obfuscated_phone", "")).strip()

        profile.obfuscated_email = obf_email
        profile.obfuscated_phone = obf_phone

        if obf_email or obf_phone:
            print(f"  ├── Obfuscated Email: {obf_email}")
            print(f"  └── Obfuscated Phone: {obf_phone}")

    except Exception:
        print("> Instagram - error")
        return False, {}

    found = bool(
        profile.username
        or profile.followers not in ("N/A", None)
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
