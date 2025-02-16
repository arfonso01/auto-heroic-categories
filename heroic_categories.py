import json
import os

from dotenv import load_dotenv

import get_categories
import get_game_modes

load_dotenv()
HEROIC_CONFIG = os.getenv("HEROIC_CONFIG")

if HEROIC_CONFIG is None:
    raise Exception("Heroic config location is missing, please set it in the env file")

heroicConfigFile = open(HEROIC_CONFIG)
heroicConfigJSON = json.load(heroicConfigFile)

if heroicConfigJSON["games"].get("customCategories") is None:
    heroicConfigJSON["games"]["customCategories"] = {}

customCategoriesSet = set(heroicConfigJSON["games"]["customCategories"])

if heroicConfigJSON["games"].get("customCategories") is None:
    heroicConfigJSON["games"]["customCategories"] = {}

customCategoriesSet = set(heroicConfigJSON["games"]["customCategories"])
genre_id_to_name = get_categories.category_dict()
game_mode_id_to_name = get_game_modes.modes_dict()


def addCategoriesToHeroicJSON(category_id_to_name):
    for categoryName in list(category_id_to_name.values()):
        if categoryName not in customCategoriesSet:
            heroicConfigJSON["games"]["customCategories"].update({categoryName: []})


addCategoriesToHeroicJSON(genre_id_to_name)
addCategoriesToHeroicJSON(game_mode_id_to_name)

with open(HEROIC_CONFIG, "w") as json_file:
    json.dump(heroicConfigJSON, json_file, indent=4, separators=(",", ": "))

heroicConfigFile.close()
