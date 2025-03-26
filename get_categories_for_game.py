from requests import post
import json
import game_library
import get_categories
import get_token
from dotenv import load_dotenv
import os
import time # progress bar
import sys # progress bar
env=os.getenv

load_dotenv()
HEROIC_CONFIG=env('HEROIC_CONFIG')
CLIENT_ID=env('CLIENT_ID')
AUTHORIZATION=get_token.authorization()

category_dict={}
categories=open(HEROIC_CONFIG)
data=json.load(categories)

# Progress bar with ETA and count
def progressBar(it, prefix="", size=60, out=sys.stdout): # Python3.6+
    if len(it) == 0:
        return
    count = len(it)
    start = time.time() # time estimate start
    def show(j):
        x = int(size*j/count)
        # time estimate calculation and string
        remaining = ((time.time() - start) / j) * (count - j)
        mins, sec = divmod(remaining, 60) # limited to minutes
        time_str = f"{int(mins):02}:{sec:03.1f}"
        print(f"{prefix}[{u'█'*x}{('.'*(size-x))}] {j}/{count} Est wait {time_str}", end='\r', file=out, flush=True)
    show(0.1) # avoid div/0
    for i, item in enumerate(it):
        yield item
        show(i+1)
    print("\n", flush=True, file=out)

for app_name in progressBar(game_library.library_dict, prefix = 'Progress:'):
    url = 'https://api.igdb.com/v4/games/?search=' + app_name + '&fields=id,name,genres'
    response = post(url, **{'headers': {'Client-ID': f'{CLIENT_ID}', 'Authorization': f'Bearer {AUTHORIZATION}'},'data': 'fields category,checksum,content_descriptions,rating,rating_cover_url,synopsis;'})

    try:
        for i in response.json()[0]['genres']:
            if i in list(get_categories.category_dict().keys()):

                if game_library.library_dict[app_name] not in data['games']['customCategories'][get_categories.category_dict()[i]]:
                    data['games']['customCategories'][get_categories.category_dict()[i]].append(game_library.library_dict[app_name])

    except IndexError:
        continue
    except KeyError:
        continue

with open(HEROIC_CONFIG, 'w') as json_file:
    json.dump(data, json_file, 
                        indent=4,  
                        separators=(',',': '))
