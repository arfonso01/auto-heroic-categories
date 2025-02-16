import os

import requests
from dotenv import load_dotenv

env = os.getenv

load_dotenv()

CLIENT_ID = env("CLIENT_ID")
CLIENT_SECRET = env("CLIENT_SECRET")


def authorization():
    url = f"https://id.twitch.tv/oauth2/token?client_id={CLIENT_ID}&client_secret={CLIENT_SECRET}&grant_type=client_credentials"
    x = requests.post(url)
    return x.json()["access_token"]
