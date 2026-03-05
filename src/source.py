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

from graphics import image_generator

FALLBACK_COVER_URL = "https://community.mp3tag.de/uploads/default/original/2X/a/acf3edeb055e7b77114f9e393d1edeeda37e50c9.png"

network = None



def main():
    global network
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

def get_album_list(artist: str, limit: int = 50) -> List[str]:
    if network is None:
        raise RuntimeError("Last.fm client is not initialized.")

    top_albums = network.get_artist(artist).get_top_albums(limit=limit)
    albums: List[str] = []
    seen = set()

    for item in top_albums:
        try:
            album_name = item.item.get_name().strip()
        except Exception:
            continue

        if not album_name or album_name in seen:
            continue

        seen.add(album_name)
        albums.append(album_name)

    return albums


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
        response = requests.get(album_cover, timeout=8)
        if response.status_code != 200:
            album_cover = FALLBACK_COVER_URL
    except:
        album_cover = FALLBACK_COVER_URL
    return album_cover

def create_tier_list():
    load_or_create_json()
    with open("albums.json") as f:
        album_file = json.load(f)

    print("TIERS - S, A, B, C, D, E")

    question = "Which artist do you want to make a tier list for?"
    artist = input(question).strip().lower()

    try:
        get_artist = network.get_artist(artist)
        artist = get_artist.get_name()
        albums_to_rank = get_album_list(artist)

        question = "What do you want to call this tier list?"
        tier_list_name = input(question).strip()

        # repeat until the user enters at least one character
        while not tier_list_name:
            print("Please enter at least one character")
            tier_list_name = input(question).strip()

        # S TIER
        s_tier_picks = create_tier_list_helper(albums_to_rank, "S Tier")

        # A TIER
        a_tier_picks = create_tier_list_helper(albums_to_rank, "A Tier")

        # B TIER
        b_tier_picks = create_tier_list_helper(albums_to_rank, "B Tier")

        # C TIER
        c_tier_picks = create_tier_list_helper(albums_to_rank, "C Tier")

        # D TIER
        d_tier_picks = create_tier_list_helper(albums_to_rank, "D Tier")

        # E TIER
        e_tier_picks = create_tier_list_helper(albums_to_rank, "E Tier")

        # check if all tiers are empty and if so, exit
        if not any([s_tier_picks, a_tier_picks, b_tier_picks, c_tier_picks, d_tier_picks, e_tier_picks]):
            print("All tiers are empty. Exiting...")
            return

        # Fetch covers once after all selections to keep tier selection responsive.
        s_tier = [{"album": album, "cover_art": get_album_cover(artist, album)} for album in s_tier_picks]
        a_tier = [{"album": album, "cover_art": get_album_cover(artist, album)} for album in a_tier_picks]
        b_tier = [{"album": album, "cover_art": get_album_cover(artist, album)} for album in b_tier_picks]
        c_tier = [{"album": album, "cover_art": get_album_cover(artist, album)} for album in c_tier_picks]
        d_tier = [{"album": album, "cover_art": get_album_cover(artist, album)} for album in d_tier_picks]
        e_tier = [{"album": album, "cover_art": get_album_cover(artist, album)} for album in e_tier_picks]

        # # add the albums that were picked to the tier list
        tier_list = {
            "tier_list_name": tier_list_name,
            "artist": artist,
            "s_tier": s_tier, 
            "a_tier": a_tier,
            "b_tier": b_tier,
            "c_tier": c_tier,
            "d_tier": d_tier,
            "e_tier": e_tier,
            "time": str(datetime.now())
        }

        # add the tier list to the json file
        album_file["tier_lists"].append(tier_list)

        # save the json file
        with open("albums.json", "w") as f:
            json.dump(album_file, f, indent=4)

        image_generator(f"{tier_list_name}.png", tier_list)
        print(f"✅ [b green]CREATED[/b green] {tier_list_name}.png")
        return

    except pylast.PyLastError:
        print("❌[b red] Artist not found [/b red]")


def see_tier_lists():
    load_or_create_json()
    with open("albums.json", "r") as f:
        data = json.load(f)

    if not data["tier_lists"]:
        print("❌ [b red]No tier lists have been created yet![/b red]")
        return

    for key in data["tier_lists"]:
        image_generator(f"{key['tier_list_name']}.png", key)
        print(f"✅ [b green]CREATED[/b green] {key['tier_list_name']}.png")

    print("✅ [b green]DONE[/b green]. Check the directory for the tier lists.")
    return

        


if __name__ == "__main__":
    main()
