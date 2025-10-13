# Auto Heroic Categories

Auto Heroic Categories, automatically categorizes your games from the 'heroic game launcher \
library' into custom categories using data from IGDB (Internet Game Database).

![](capture.gif)

# Metacritic Scores

Automatic categorizes your games based on the Metacritic portal.

## How it works

- It tries to parse the game page based on game's titles. If it's unable to find it will use metacritic search page to find an occurence.
- The first occurrence found will be used to collect the scores. 
- The scores found will saved in the `PATHO` path as `metacritic.json` database file.
- The collected scores will be used to assign the proper score category:

```
metascore_0s => from 0 to 19
metascore_10s => from 10 to 19
...
metascore_90s => from 90 to 99
metascore_100s => 100
```
and userscores:

```
userscore_0s => from 0 to 
userscore_10s => from 10 to 19
...
userscore_90s => from 90 to 99
userscore_100s => 100
```

### Requirements
* `sudo apt install wget git python3 python3-venv`.
* `git clone https://github.com/arfonso01/auto-heroic-categories.git`. 
* You need the igdb api, you can get access by following the steps in this [link](https://api-docs.igdb.com/?getting-started#account-creation)

### Configuration
The script requires the following environment variables, you rename env_exaple to .env and edit:
* `CLIENT_ID`: IGDB API client ID, get it [here](https://dev.twitch.tv/console/apps/)
* `CLIENT_SECRET`: IGDB API client secret, create it [here](https://dev.twitch.tv/console/apps/)
* `PATHO`: path to the JSON files containing the games names
* `HEROIC_CONFIG`: path to the JSON file containing the custom categories
* `METACRITIC_ENABLED`: enable metacritic scores retrieval and add metascore_XXs and userscore_XXs as custom categories (True or False, default False)
* `METACRITIC_REFRESH`: it will try to retrieve again all the games that has a score of 'tbd' (to be defined) that were skipped previously (True or False, default False)

### How to use
* Give permissions to the run.sh file: `chmod +x run.sh`
* Execute: `./run.sh`
