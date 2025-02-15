import json
import os

from dotenv import load_dotenv
from requests import post

import game_library
import get_categories
import get_token

env = os.getenv

load_dotenv()
HEROIC_CONFIG = env("HEROIC_CONFIG")
CLIENT_ID = env("CLIENT_ID")
AUTHORIZATION = get_token.authorization()

category_dict = {}
categories = open(HEROIC_CONFIG)
data = json.load(categories)

for app_name in game_library.library_dict:
    url = "https://api.igdb.com/v4/games/?search=" + app_name + "&fields=id,name,genres"
    response = post(
        url,
        **{
            "headers": {
                "Client-ID": f"{CLIENT_ID}",
                "Authorization": f"Bearer {AUTHORIZATION}",
            },
            "data": "fields category,checksum,content_descriptions,rating,rating_cover_url,synopsis;",
        },
    )

    try:
        for i in response.json()[0]["genres"]:
            if i in list(get_categories.category_dict().keys()):
                if (
                    game_library.library_dict[app_name]
                    not in data["games"]["customCategories"][
                        get_categories.category_dict()[i]
                    ]
                ):
                    data["games"]["customCategories"][
                        get_categories.category_dict()[i]
                    ].append(game_library.library_dict[app_name])

    except IndexError:
        continue
    except KeyError:
        continue

with open(HEROIC_CONFIG, "w") as json_file:
    json.dump(data, json_file, indent=4, separators=(",", ": "))
