import json
import os
from datetime import datetime
from io import BytesIO
from typing import List

import pylast
import requests
from pick import pick
from PIL import Image, ImageDraw, ImageFont
from rich import print
from rich.panel import Panel
from rich.table import Table
from pathlib import Path
from dotenv import load_dotenv





def main():
    print("Hello from Tier List!")
    # Load .env from project root so it works regardless of launch directory.
    load_dotenv(Path(__file__).resolve().parents[1] / ".env")

    # Get API key from environment
    API_KEY = os.getenv("LASTFM_API_KEY")
    API_SECRET = os.getenv("LASTFM_API_SECRET")

    if API_KEY and API_SECRET:
        print("Got the API key and secret")
    else:
        print("Where is the API key or secret")
        return

    network = pylast.LastFMNetwork(api_key=API_KEY, api_secret=API_SECRET)
    start()

def start():
    global network
    startup_question = "What Do You Want To Do?"
    options = ["Rate by Album", "Rate Songs", "See Albums Rated", "See Songs Rated", "Make a Tier List", "See Created Tier Lists", "EXIT"]
    selected_option, index = pick(options, startup_question, indicator="→")

    if index == 0:
        rate_by_album()
    elif index == 1:
        rate_by_song()
    elif index == 2:
        see_albums_rated()
    elif index == 3:
        see_songs_rated()
    elif index == 4:
        create_tier_list()
    elif index == 5:
        see_tier_lists()
    elif index == 6:
        exit()

def load_or_create_json() -> None:
    if os.path.exists("albums.json"):
        with open("albums.json") as f:
            ratings = json.load(f)
    else:
        # create a new json file with empty dict
        with open("albums.json", "w") as f:
            ratings = {"album_ratings": [], "song_ratings": [], "tier_lists": []}
            json.dump(ratings, f)


def create_tier_list_helper(albums_to_rank, tier_name):
    # if there are no more albums to rank, return an empty list
    if not albums_to_rank:
        return []

    question = f"Select the albums you want to rank in  {tier_name}"
    tier_picks = pick(options=albums_to_rank, title=question, multiselect=True, indicator="→", min_selection_count=0)
    tier_picks = [x[0] for x in tier_picks]

    for album in tier_picks:
        albums_to_rank.remove(album)

    return tier_picks 

def get_album_cover(artist, album):
    album = network.get_album(artist, album)
    album_cover = album.get_cover_image()
    # check if it is a valid url
    try:
        response = requests.get(album_cover)
        if response.status_code != 200:
            album_cover = "https://community.mp3tag.de/uploads/default/original/2X/a/acf3edeb055e7b77114f9e393d1edeeda37e50c9.png"
    except:
        album_cover = "https://community.mp3tag.de/uploads/default/original/2X/a/acf3edeb055e7b77114f9e393d1edeeda37e50c9.png"
    return album_cover

if __name__ == "__main__":
    main()
