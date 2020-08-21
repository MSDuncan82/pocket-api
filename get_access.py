import dotenv
import os
import requests


def get_request_token(
    consumer_key, redirect_uri, api_endpoint="https://getpocket.com/v3/oauth/request"
):
    """Test docs"""

    params = {"consumer_key": consumer_key, "redirect_uri": redirect_uri}

    response = requests.post(f"{api_endpoint}", params=params)

    request_token = response.content.decode().split("=")[1]
    import ipdb

    ipdb.set_trace()
    return request_token


def get_access_token(
    request_token, consumer_key, api_endpoint="https://getpocket.com/v3/oauth/authorize"
):

    params = {"consumer_key": consumer_key, "code": request_token}

    response = requests.post(api_endpoint, params=params)
    import ipdb

    ipdb.set_trace()
    return response


if __name__ == "__main__":

    dotenv.load_dotenv()

    CONSUMER_KEY = os.environ["CONSUMER_KEY"]
    REDIRECT_URI = "pocketauth"

    request_token = get_request_token(
        consumer_key=CONSUMER_KEY, redirect_uri=REDIRECT_URI
    )

    access = get_access_token(request_token, CONSUMER_KEY)

    print(access)
