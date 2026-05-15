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

        profile.obfuscated_email = user.get("obfuscated_email", "")
        profile.obfuscated_phone = str(user.get("obfuscated_phone", "")).strip()

        if profile.obfuscated_email or profile.obfuscated_phone:
            print(f"  ├── Obfuscated Email: {profile.obfuscated_email}")
            print(f"  └── Obfuscated Phone: {profile.obfuscated_phone}")

    except Exception:
        print("> Instagram - error")
        return False, {}

    has_real_data = any([
        profile.followers not in ("N/A", None),
        profile.following not in ("N/A", None),
        profile.full_name.strip() != "",
        profile.biography.strip() != "",
        profile.is_verified is True,
        profile.obfuscated_email,
        profile.obfuscated_phone
    ])

    found = bool(user and has_real_data)

    data = {
        "username": profile.username,
        "user_id": profile.user_id,
        "full_name": profile.full_name,
        "followers": profile.followers,
        "following": profile.following,
        "verified": profile.is_verified,
        "obfuscated_email": profile.obfuscated_email,
        "obfuscated_phone": profile.obfuscated_phone,
    }

    return found, data
