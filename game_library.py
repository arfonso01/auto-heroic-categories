import json
from dotenv import load_dotenv
import os

env=os.getenv

load_dotenv()

def open_library(library):
    try:
        return open(library, encoding="utf8")
    except FileNotFoundError as e:
        print("Some library locations not found: "+str(e))
    except TypeError as e:
        print("Check your .env files has been updated")
        exit(1)

GOG_LIBRARY=os.path.join(env('PATHO'), env('GOG_LIBRARY'))
AMAZON_LIBRARY=os.path.join(env('PATHO'), env('AMAZON_LIBRARY'))
EPIC_LIBRARY=os.path.join(env('PATHO'), env('EPIC_LIBRARY'))

GOG_LIBRARY=open_library(GOG_LIBRARY)
AMAZON_LIBRARY=open_library(AMAZON_LIBRARY)
EPIC_LIBRARY=open_library(EPIC_LIBRARY)

library_dict={}

def library(library,root_json: str):
    try:
        data=json.load(library)
        for i in data[root_json]:
            if 'gog' in str(library):
                appname=i['app_name']+'_gog'
            if 'legendary' in str(library):
                appname=i['app_name']+'_legendary'
            if 'nile' in str(library):
                appname=i['app_name']+'_nile' 

            try:
                if i['app_name']!= 'gog-redist_gog':
                    library_dict.update({i['title']:appname})
            except KeyError as k:
                print(f"KeyError: {k} in {i['title']}. Skipping this entry.")
                continue

        library.close()
        return library_dict
    except (KeyError, AttributeError) as e:
        print(str(e)+'. Game library likely not found.')

def get_titles():
    titles = {}
    gog_titles = library(GOG_LIBRARY, 'games')
    epic_titles = library(EPIC_LIBRARY, 'library')
    amazon_titles = library(AMAZON_LIBRARY, 'library')
    titles.update(gog_titles)
    titles.update(epic_titles)
    titles.update(amazon_titles)
    sorted_titles = dict(sorted(titles.items(), key=lambda x: x[0].lower()))
    #with open("games_list.json", "w") as f:
    #    json.dump(sorted_titles, f, indent=2, ensure_ascii=False)
    return sorted_titles

def get_title_names():
    titles = get_titles()
    #print(titles)
    return list(titles.keys())

if __name__ == "__main__":
    print(json.dumps(get_titles(), indent=2, ensure_ascii=False))    
    #print(get_title_names())
