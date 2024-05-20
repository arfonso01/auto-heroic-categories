#!/bin/bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 heroic_categories.py
python3 get_categories_for_game.py
deactivate
exit
