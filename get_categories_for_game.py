import json
import os

from dotenv import load_dotenv
from requests import post

import game_library
import get_categories
import get_game_modes
import get_token

load_dotenv()
HEROIC_CONFIG = os.getenv("HEROIC_CONFIG")
CLIENT_ID = os.getenv("CLIENT_ID")
AUTHORIZATION = get_token.authorization()

if HEROIC_CONFIG is None:
    raise Exception("Heroic config location is missing, please set it in the env file")

heroicConfigFile = open(HEROIC_CONFIG)
heroicConfigJSON = json.load(heroicConfigFile)


def appendGameToCategory(id, category_id_to_name, game_name):
    game_id = game_library.library_dict[game_name]
    customCategories = heroicConfigJSON["games"]["customCategories"]

    if id in list(category_id_to_name.keys()):
        category_name = category_id_to_name[id]
        if game_id not in customCategories[category_name]:
            customCategories[category_name].append(game_id)


genre_id_to_name = get_categories.category_dict()
game_mode_id_to_name = get_game_modes.modes_dict()

for game_name in game_library.library_dict:
    print(f"Requesting information for {game_name} from IGDB")
    url = f"https://api.igdb.com/v4/games/?search={game_name}&fields=id,name,genres,game_modes"
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
        for genre_id in response.json()[0]["genres"]:
            appendGameToCategory(genre_id, genre_id_to_name, game_name)

        for game_mode_id in response.json()[0]["game_modes"]:
            appendGameToCategory(game_mode_id, game_mode_id_to_name, game_name)

    except IndexError:
        continue
    except KeyError:
        continue

with open(HEROIC_CONFIG, "w") as json_file:
    json.dump(heroicConfigJSON, json_file, indent=4, separators=(",", ": "))
