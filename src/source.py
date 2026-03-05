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

        # keep only the album name by splitting the string at the first - and removing the first element
        albums_to_rank = [x.split(" - ", 1)[1] for x in albums_to_rank[1:]]

        question = "What do you want to call this tier list?"
        tier_list_name = input(question).strip()

        # repeat until the user enters at least one character
        while not tier_list_name:
            print("Please enter at least one character")
            tier_list_name = input(question).strip()

        # S TIER
        question = "Select the albums you want to rank in S Tier:"
        s_tier_picks = create_tier_list_helper(albums_to_rank, "S Tier")
        s_tier_covers = [get_album_cover(artist, album) for album in s_tier_picks]
        s_tier = [{"album":album,"cover_art": cover} for album, cover in zip(s_tier_picks, s_tier_covers)]

        # A TIER
        question = "Select the albums you want to rank in A Tier:"
        a_tier_picks = create_tier_list_helper(albums_to_rank, "A Tier")
        a_tier_covers = [get_album_cover(artist, album) for album in a_tier_picks]
        a_tier = [{"album":album,"cover_art": cover} for album, cover in zip(a_tier_picks, a_tier_covers)]

        # B TIER
        question = "Select the albums you want to rank in B Tier:"
        b_tier_picks = create_tier_list_helper(albums_to_rank, "B Tier")
        b_tier_covers = [get_album_cover(artist, album) for album in b_tier_picks]
        b_tier = [{"album":album,"cover_art": cover} for album, cover in zip(b_tier_picks, b_tier_covers)]

        # C TIER
        question = "Select the albums you want to rank in C Tier:"
        c_tier_picks = create_tier_list_helper(albums_to_rank, "C Tier")
        c_tier_covers = [get_album_cover(artist, album) for album in c_tier_picks]
        c_tier = [{"album":album,"cover_art": cover} for album, cover in zip(c_tier_picks, c_tier_covers)]

        # D TIER
        question = "Select the albums you want to rank in D Tier:"
        d_tier_picks = create_tier_list_helper(albums_to_rank, "D Tier")
        d_tier_covers = [get_album_cover(artist, album) for album in d_tier_picks] 
        d_tier = [{"album":album,"cover_art": cover} for album, cover in zip(d_tier_picks, d_tier_covers)]
        # E TIER
        question = "Select the albums you want to rank in E Tier:"
        e_tier_picks = create_tier_list_helper(albums_to_rank, "E Tier")
        e_tier_covers = [get_album_cover(artist, album) for album in e_tier_picks]
        e_tier = [{"album":album,"cover_art": cover} for album, cover in zip(e_tier_picks, e_tier_covers)]

        # check if all tiers are empty and if so, exit
        if not any([s_tier_picks, a_tier_picks, b_tier_picks, c_tier_picks, d_tier_picks, e_tier_picks]):
            print("All tiers are empty. Exiting...")
            return


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

        return

    except pylast.PyLastError:
        print("❌[b red] Artist not found [/b red]")


if __name__ == "__main__":
    main()
