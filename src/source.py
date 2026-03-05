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

# Load .env from project root so it works regardless of launch directory.
load_dotenv(Path(__file__).resolve().parents[1] / ".env")

# Get API key from environment
API_KEY = os.getenv("LASTFM_API_KEY")

print("Got the API key") if API_KEY else print("Where is the API key")

def main():
    print("Hello from tierlist!")


if __name__ == "__main__":
    main()
