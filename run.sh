#!/bin/bash
# check if UV IS INSTALLED THEN DO
if  command -v uv &> /dev/null
then # https://docs.astral.sh/uv/ Faster and better pip
    echo "UV is installed. Using uv to install"
    uv sync
    uv run env_check.py
    uv run heroic_categories.py
    uv run get_categories_for_game.py
    uv run metacritic.py
else
    echo "UV is not installed. Using pip and python3 to install"
    python3 -m pip install uv
    python3 -m pip install -r requirements.txt
    python env_check.py
    python3 heroic_categories.py
    python3 get_categories_for_game.py
    python3 metacritic.py
    deactivate
fi

# python3 -m venv venv
# source venv/bin/activate
# pip install -r requirements.txt

exit
