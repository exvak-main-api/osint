from lib.requests import Request

async def instagram(target: str):

    try:
        req = await Request(
            "https://www.instagram.com/accounts/emailsignup/"
        ).get()

        try:
            csrf_token = req.cookies.get('csrftoken')
        except:
            return False

        if not csrf_token:
            return False

        data = {
            'email': target,
            'first_name': '',
            'username': '',
            'opt_into_one_tap': False
        }

        headers = {
            'x-csrftoken': csrf_token
        }

        r = await Request(
            "https://www.instagram.com/api/v1/web/accounts/web_create_ajax/attempt/",
            headers=headers,
            data=data
        ).post()

        try:
            response = r.json()
        except:
            return False

        try:
            code = (
                response
                .get('errors', {})
                .get('email', [{}])[0]
                .get('code')
            )

            if code == 'email_is_taken':
                return True

            return False

        except:
            return False

    except:
        return False
