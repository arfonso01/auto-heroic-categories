# Auto Heroic Categories

Auto Heroic Categories categories your games from the 'heroic game launcher \
library' into custom categories using data from IGDB (Internet Game Database).

![](capture.gif)

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

### How to use
* Give permissions to the run.sh file: `chmod +x run.sh`
* Execute: `./run.sh`
