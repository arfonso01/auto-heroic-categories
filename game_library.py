import json
from dotenv import load_dotenv
import os

env=os.getenv

load_dotenv()

GOG_LIBRARY=os.path.join(env('PATHO'), env('GOG_LIBRARY'))
AMAZON_LIBRARY=os.path.join(env('PATHO'), env('AMAZON_LIBRARY'))
EPIC_LIBRARY=os.path.join(env('PATHO'), env('EPIC_LIBRARY'))

GOG_LIBRARY=open(GOG_LIBRARY, encoding="utf8")
AMAZON_LIBRARY=open(AMAZON_LIBRARY, encoding="utf8")
EPIC_LIBRARY=open(EPIC_LIBRARY, encoding="utf8")

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
    except KeyError as e:
        print(e)

library(GOG_LIBRARY, 'games')
library(AMAZON_LIBRARY, 'library')
library(EPIC_LIBRARY, 'library')
