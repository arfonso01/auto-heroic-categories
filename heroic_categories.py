import json
import os

from dotenv import load_dotenv

import get_categories

env = os.getenv

load_dotenv()
HEROIC_CONFIG = env("HEROIC_CONFIG")

heroicConfigFile = open(HEROIC_CONFIG)
heroicConfigJSON = json.load(heroicConfigFile)
customCategoriesSet = set(heroicConfigJSON["games"]["customCategories"])

for i in list(get_categories.category_dict().values()):
    if i not in customCategoriesSet:
        heroicConfigJSON["games"]["customCategories"].update({i: []})

list_data = list(customCategoriesSet)

with open(HEROIC_CONFIG, "w") as json_file:
    json.dump(heroicConfigJSON, json_file, indent=4, separators=(",", ": "))

heroicConfigFile.close()
