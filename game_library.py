import json
from dotenv import load_dotenv
import os

env=os.getenv

load_dotenv()

GOG_LIBRARY=env('PATHO') + env('GOG_LIBRARY')
AMAZON_LIBRARY=env('PATHO') + env('AMAZON_LIBRARY')
EPIC_LIBRARY=env('PATHO') + env('EPIC_LIBRARY')

GOG_LIBRARY=open(GOG_LIBRARY)
AMAZON_LIBRARY=open(AMAZON_LIBRARY)
EPIC_LIBRARY=open(EPIC_LIBRARY)

library_dict={}

def library(library,root_json: str):
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

library(GOG_LIBRARY, 'games')
library(AMAZON_LIBRARY, 'library')
library(EPIC_LIBRARY, 'library')
