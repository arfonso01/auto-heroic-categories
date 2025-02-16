import json
import os

from dotenv import load_dotenv
from requests import post

import game_library
import get_categories
import get_token

load_dotenv()
HEROIC_CONFIG = os.getenv("HEROIC_CONFIG")
CLIENT_ID = os.getenv("CLIENT_ID")
AUTHORIZATION = get_token.authorization()

if HEROIC_CONFIG is None:
    raise Exception("Heroic config location is missing, please set it in the env file")

heroicConfigFile = open(HEROIC_CONFIG)
heroicConfigJSON = json.load(heroicConfigFile)

for game_name in game_library.library_dict:
    url = f"https://api.igdb.com/v4/games/?search={game_name}&fields=id,name,genres"
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
                    game_library.library_dict[game_name]
                    not in heroicConfigJSON["games"]["customCategories"][
                        get_categories.category_dict()[i]
                    ]
                ):
                    heroicConfigJSON["games"]["customCategories"][
                        get_categories.category_dict()[i]
                    ].append(game_library.library_dict[game_name])

    except IndexError:
        continue
    except KeyError:
        continue

with open(HEROIC_CONFIG, "w") as json_file:
    json.dump(heroicConfigJSON, json_file, indent=4, separators=(",", ": "))
