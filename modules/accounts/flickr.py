from lib.requests import Request
import re

async def flickr(target: str):

    try:
        r = await Request("https://www.flickr.com/").get()

        key_pattern = r'[a-f0-9]{32}'
        keys = re.findall(key_pattern, r.text)

        api_keys = set(keys)

        if not api_keys:
            return False

        for key in api_keys:

            api = "https://api.flickr.com/services/rest"

            params = {
                'username': target,
                'exact': 0,
                'extras': 'path_alias%2Crev_ignored%2Crev_contacts%2Cis_pro%2Cicon_urls%2Clocation%2Crev_contact_count%2Cuse_vespa%2Cdate_joined',
                'per_page': 5,
                'page': 0,
                'show_more': 1,
                'perPage': 50,
                'loadFullContact': 1,
                'viewerNSID': None,
                'method': 'flickr.people.search',
                'api_key': key,
                'format': 'json',
                'hermes': 1,
                'hermesClient': 1,
                'nojsoncallback': 1
            }

            try:
                r = await Request(api, params=params).get()
                data = r.json()

                if (
                    data.get('people')
                    and data['people'].get('person')
                    and len(data['people']['person']) > 0
                ):
                    return True

            except:
                continue

        return False

    except:
        return False
