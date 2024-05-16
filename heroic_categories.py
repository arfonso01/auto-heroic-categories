import json
import get_categories
from dotenv import load_dotenv
import os
env=os.getenv

load_dotenv()
HEROIC_CONFIG=env('HEROIC_CONFIG')

custom_categories=open(HEROIC_CONFIG)
data=json.load(custom_categories)
set_data=set(data['games']['customCategories'])

for i in list(get_categories.category_dict().values()):
    if i not in set_data:
        data['games']['customCategories'].update({i:[]})

list_data=list(set_data)

with open(HEROIC_CONFIG, 'w') as json_file:
    json.dump(data, json_file, 
                        indent=4,  
                        separators=(',',': '))

custom_categories.close()
