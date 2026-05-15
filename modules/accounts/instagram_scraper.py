import asyncio
from instaloader import Instaloader, Profile


class IGCollector:
    def __init__(self, username: str):
        self.username = username
        self.loader = Instaloader()

    def run(self):
        profile = Profile.from_username(self.loader.context, self.username)

        return {
            "username": profile.username,
            "full_name": profile.full_name,
            "followers": profile.followers,
            "following": profile.followees,
            "posts": profile.mediacount,
            "bio": profile.biography,
            "is_private": profile.is_private,
            "is_verified": profile.is_verified,
            "is_business": profile.is_business_account,
            "external_url": profile.external_url,
            "business_type": profile.business_category_name,
        }


async def instagram_scraper(target: str):
    try:
        collector = IGCollector(target)

        data = await asyncio.to_thread(collector.run)

        if not data:
            print("> Instagram - not found")
            return False, {}

        print("> Instagram")
        print(f"  ├── Username: {data['username']}")
        print(f"  ├── Name: {data['full_name']}")
        print(f"  ├── Followers: {data['followers']}")
        print(f"  ├── Following: {data['following']}")
        print(f"  ├── Posts: {data['posts']}")
        print(f"  ├── Bio: {data['bio']}")
        print(f"  ├── Business Account: {data['is_business']}")
        print(f"  ├── Verified: {data['is_verified']}")
        print(f"  ├── Private: {data['is_private']}")
        print(f"  └── External URL: {data['external_url']}")

        return True, data

    except Exception:
        print("> Instagram - error")
        return False, {}
