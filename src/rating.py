import json
import os
from datetime import datetime

import pylast
from pick import pick
from rich import print
from rich.table import Table

DATA_FILE = "albums.json"


def load_or_create_json() -> dict:
    default_data = {"album_ratings": [], "song_ratings": [], "tier_lists": []}

    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w") as f:
            json.dump(default_data, f, indent=4)
        return default_data

    with open(DATA_FILE) as f:
        data = json.load(f)

    changed = False
    for key in default_data:
        if key not in data or not isinstance(data[key], list):
            data[key] = []
            changed = True

    if changed:
        with open(DATA_FILE, "w") as f:
            json.dump(data, f, indent=4)

    return data


def _save_json(data: dict) -> None:
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)


def _normalize(value: str) -> str:
    return value.strip().casefold()


def _time_key(entry: dict) -> datetime:
    raw_time = entry.get("time", "")
    try:
        return datetime.fromisoformat(raw_time)
    except ValueError:
        return datetime.min


def _get_top_album_names(network: pylast.LastFMNetwork, artist: str, limit: int = 50) -> list[str]:
    top_albums = network.get_artist(artist).get_top_albums(limit=limit)
    albums: list[str] = []
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


def _get_top_track_names(network: pylast.LastFMNetwork, artist: str, limit: int = 100) -> list[str]:
    top_tracks = network.get_artist(artist).get_top_tracks(limit=limit)
    tracks: list[str] = []
    seen = set()

    for item in top_tracks:
        try:
            track_name = item.item.get_name().strip()
        except Exception:
            continue

        if not track_name or track_name in seen:
            continue

        seen.add(track_name)
        tracks.append(track_name)

    return tracks


def _pick_rating(prompt_label: str) -> int:
    options = [str(i) for i in range(10, 0, -1)]
    selected_rating, _ = pick(options, f"Rate {prompt_label} (1-10)", indicator="→")
    return int(selected_rating)


def _upsert_album_rating(data: dict, artist: str, album: str, rating: int) -> str:
    now = datetime.now().isoformat(timespec="seconds")
    for entry in data["album_ratings"]:
        if _normalize(entry.get("artist", "")) == _normalize(artist) and _normalize(entry.get("album", "")) == _normalize(album):
            entry["rating"] = rating
            entry["time"] = now
            return "updated"

    data["album_ratings"].append(
        {
            "artist": artist,
            "album": album,
            "rating": rating,
            "time": now,
        }
    )
    return "added"


def _upsert_song_rating(data: dict, artist: str, song: str, rating: int) -> str:
    now = datetime.now().isoformat(timespec="seconds")
    for entry in data["song_ratings"]:
        if _normalize(entry.get("artist", "")) == _normalize(artist) and _normalize(entry.get("song", "")) == _normalize(song):
            entry["rating"] = rating
            entry["time"] = now
            return "updated"

    data["song_ratings"].append(
        {
            "artist": artist,
            "song": song,
            "rating": rating,
            "time": now,
        }
    )
    return "added"


def rate_by_album(network: pylast.LastFMNetwork) -> None:
    artist_input = input("Artist for album rating: ").strip()
    if not artist_input:
        print("❌ [b red]Please enter an artist name.[/b red]")
        return

    try:
        artist = network.get_artist(artist_input).get_name()
        albums = _get_top_album_names(network, artist)
    except pylast.PyLastError:
        print("❌ [b red]Artist not found.[/b red]")
        return

    if not albums:
        print("❌ [b red]No albums found for this artist.[/b red]")
        return

    selected_album, _ = pick(albums, f"Select an album by {artist}", indicator="→")
    rating = _pick_rating(f"album '{selected_album}'")

    data = load_or_create_json()
    result = _upsert_album_rating(data, artist, selected_album, rating)
    _save_json(data)

    print(f"✅ [b green]Album rating {result}:[/b green] {artist} - {selected_album} = {rating}/10")


def rate_by_song(network: pylast.LastFMNetwork) -> None:
    artist_input = input("Artist for song rating: ").strip()
    if not artist_input:
        print("❌ [b red]Please enter an artist name.[/b red]")
        return

    try:
        artist = network.get_artist(artist_input).get_name()
        tracks = _get_top_track_names(network, artist)
    except pylast.PyLastError:
        print("❌ [b red]Artist not found.[/b red]")
        return

    if not tracks:
        print("❌ [b red]No songs found for this artist.[/b red]")
        return

    selected_song, _ = pick(tracks, f"Select a song by {artist}", indicator="→")
    rating = _pick_rating(f"song '{selected_song}'")

    data = load_or_create_json()
    result = _upsert_song_rating(data, artist, selected_song, rating)
    _save_json(data)

    print(f"✅ [b green]Song rating {result}:[/b green] {artist} - {selected_song} = {rating}/10")


def see_albums_rated() -> None:
    data = load_or_create_json()
    ratings = sorted(data["album_ratings"], key=_time_key, reverse=True)

    if not ratings:
        print("❌ [b red]No album ratings yet.[/b red]")
        return

    table = Table(title="Album Ratings")
    table.add_column("Artist")
    table.add_column("Album")
    table.add_column("Rating")
    table.add_column("Rated At")

    for entry in ratings:
        table.add_row(
            entry.get("artist", ""),
            entry.get("album", ""),
            str(entry.get("rating", "")),
            entry.get("time", ""),
        )

    print(table)


def see_songs_rated() -> None:
    data = load_or_create_json()
    ratings = sorted(data["song_ratings"], key=_time_key, reverse=True)

    if not ratings:
        print("❌ [b red]No song ratings yet.[/b red]")
        return

    table = Table(title="Song Ratings")
    table.add_column("Artist")
    table.add_column("Song")
    table.add_column("Rating")
    table.add_column("Rated At")

    for entry in ratings:
        table.add_row(
            entry.get("artist", ""),
            entry.get("song", ""),
            str(entry.get("rating", "")),
            entry.get("time", ""),
        )

    print(table)
