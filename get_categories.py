import os
from functools import lru_cache

from dotenv import load_dotenv
from requests import post

import get_token

env = os.getenv

load_dotenv()
CLIENT_ID = env("CLIENT_ID")
AUTHORIZATION = get_token.authorization()


@lru_cache(maxsize=128)
def category_dict():
    my_dict = {}
    response = post(
        "https://api.igdb.com/v4/genres",
        **{
            "headers": {
                "Client-ID": f"{CLIENT_ID}",
                "Authorization": f"Bearer {AUTHORIZATION}",
            },
            "data": "fields name,id; limit 100;",
        },
    )
    for i in response.json():
        my_dict.update({i["id"]: i["name"]})

    return my_dict
