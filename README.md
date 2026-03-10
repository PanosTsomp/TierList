# TierList

TierList is a Python CLI app for rating music and generating album tier list images using Last.fm data.

## What This Project Is

The app connects to the Last.fm API, fetches an artist's top albums/tracks, and lets you:

- Rate albums (1-10)
- Rate songs (1-10)
- View saved ratings
- Build album tier lists (S/A/B/C/D/E)
- Export tier lists as PNG images

All ratings and tier list data are stored locally in `albums.json`.

## Requirements

- Python `3.14+` (as defined in `pyproject.toml`)
- A Last.fm API key and secret
- Internet connection (for Last.fm data and cover art)

## Setup

1. Create a `.env` file in the project root:

```env
LASTFM_API_KEY=your_key_here
LASTFM_API_SECRET=your_secret_here
```

2. Install dependencies (recommended with `uv`):

```bash
uv sync
```

Alternative (venv + pip):

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

## How To Run

Run the app from the project root:

```bash
uv run python src/source.py
```

If you already activated a virtual environment:

```bash
python src/source.py
```

## Features

- Interactive terminal menu (arrow keys + enter)
- Album rating flow:
  - Select artist
  - Pick from top albums
  - Save/update rating
- Song rating flow:
  - Select artist
  - Pick from top tracks
  - Save/update rating
- Ratings viewer:
  - Album ratings table
  - Song ratings table
- Tier list builder:
  - Assign albums into S/A/B/C/D/E tiers
  - Fetch album covers
  - Generate a PNG tier board
- Tier list regeneration:
  - Re-generate images from saved tier list entries

## Scripts

- `src/source.py`
  - Main entry point
  - Loads environment variables
  - Creates Last.fm client
  - Shows main menu and orchestrates all actions
- `src/rating.py`
  - Handles rating logic and persistence
  - Creates/loads `albums.json`
  - Adds/updates album and song ratings
  - Prints ratings using rich tables
- `src/graphics.py`
  - Generates tier list images with Pillow
  - Draws tier rows and album covers
  - Saves `<tier_list_name>.png`

## Data And Outputs

- `albums.json`: persistent storage for:
  - `album_ratings`
  - `song_ratings`
  - `tier_lists`
- `<tier_list_name>.png`: generated image output for each tier list

## Notes

- If a cover art URL fails, a fallback image is used.
- If an output PNG already exists, the generator currently skips overwriting it.


TierList Creator
Author: PANAGIOTIS ILIAS TSOMPANOGLOU 
GitHub:  https://github.com/PanosTsomp
License: MIT