#!/bin/bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python heroic_categories.py
python get_categories_for_game.py
deactivate
exit
