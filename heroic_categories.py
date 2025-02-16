import json
import os

from dotenv import load_dotenv

import get_categories

load_dotenv()
HEROIC_CONFIG = os.getenv("HEROIC_CONFIG")

if HEROIC_CONFIG is None:
    raise Exception("Heroic config location is missing, please set it in the env file")

heroicConfigFile = open(HEROIC_CONFIG)
heroicConfigJSON = json.load(heroicConfigFile)

if heroicConfigJSON["games"].get("customCategories") is None:
    heroicConfigJSON["games"]["customCategories"] = {}

customCategoriesSet = set(heroicConfigJSON["games"]["customCategories"])

for i in list(get_categories.category_dict().values()):
    if i not in customCategoriesSet:
        heroicConfigJSON["games"]["customCategories"].update({i: []})

with open(HEROIC_CONFIG, "w") as json_file:
    json.dump(heroicConfigJSON, json_file, indent=4, separators=(",", ": "))

heroicConfigFile.close()
