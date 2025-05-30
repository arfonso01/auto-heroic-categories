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
            except KeyError:
                continue

        library.close()
    except (KeyError, AttributeError) as e:
        print(str(e)+'. Game library likely not found.')

library(GOG_LIBRARY, 'games')
library(AMAZON_LIBRARY, 'library')
library(EPIC_LIBRARY, 'library')
