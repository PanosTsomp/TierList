import os
from io import BytesIO

import requests
from PIL import Image, ImageDraw, ImageFont


def image_generator(file_name, data):

    # return if the file already exists
    if os.path.exists(file_name):
        return

    # Set the image size and font
    image_width = 1920
    image_height = 5000
    text_font_size = 30
    tier_font_size = 44
    try:
        # Prefer a bundled/common font with explicit sizing.
        font = ImageFont.truetype("DejaVuSans.ttf", text_font_size)
        tier_font = ImageFont.truetype("DejaVuSans-Bold.ttf", tier_font_size)
    except OSError:
        try:
            font = ImageFont.truetype("arial.ttf", text_font_size)
            tier_font = ImageFont.truetype("arial.ttf", tier_font_size)
        except OSError:
            font = ImageFont.load_default()
            tier_font = ImageFont.load_default()

    # Make a new image with the size and background color black
    image = Image.new("RGB", (image_width, image_height), "black")
    text_cutoff_value = 20

    #Initialize variables for row and column positions
    row_pos = 0
    col_pos = 0
    increment_size = 200

    def draw_tier_label(draw, x, y, label, fill, text_fill):
        draw.rectangle((x, y, x + increment_size, y + increment_size), fill=fill)
        left, top, right, bottom = draw.textbbox((0, 0), label, font=tier_font)
        text_w = right - left
        text_h = bottom - top
        text_x = x + (increment_size - text_w) // 2
        text_y = y + (increment_size - text_h) // 2
        draw.text((text_x, text_y), label, font=tier_font, fill=text_fill)

    """S Tier"""
    # leftmost side - make a square with text centered inside and fill color
    if col_pos == 0:
        draw = ImageDraw.Draw(image)
        draw_tier_label(draw, col_pos, row_pos, "S Tier", "red", "white")
        col_pos += increment_size

    for album in data["s_tier"]:
        # Get the cover art
        try:
            response = requests.get(album["cover_art"], timeout=8)
            response.raise_for_status()
            cover_art = Image.open(BytesIO(response.content))
        except Exception:
            cover_art = Image.new("RGB", (increment_size, increment_size), "gray")

        # Resize the cover art
        cover_art = cover_art.resize((increment_size, increment_size))

        # Paste the cover art onto the base image
        image.paste(cover_art, (col_pos, row_pos))

        # Draw the album name on the image with the font size 10 and background color white
        draw = ImageDraw.Draw(image)

        # Get the album name
        name = album["album"]
        if len(name) > text_cutoff_value:
            name = f"{name[:text_cutoff_value]}..."

        draw.text((col_pos, row_pos + increment_size), name, font=font, fill="white")

        # Increment the column position
        col_pos += 200
        # check if the column position is greater than the image width
        if col_pos > image_width - increment_size:
            # add a new row
            row_pos += increment_size + 50
            col_pos = 0 

    # add a new row to separate the tiers
    row_pos += increment_size + 50
    col_pos = 0

    """A TIER"""
    if col_pos == 0:
        draw = ImageDraw.Draw(image)
        draw_tier_label(draw, col_pos, row_pos, "A Tier", "orange", "white")
        col_pos += increment_size

    for album in data["a_tier"]:
        try:
            response = requests.get(album["cover_art"], timeout=8)
            response.raise_for_status()
            cover_art = Image.open(BytesIO(response.content))
        except Exception:
            cover_art = Image.new("RGB", (increment_size, increment_size), "gray")
        cover_art = cover_art.resize((increment_size, increment_size))
        image.paste(cover_art, (col_pos, row_pos))
        draw = ImageDraw.Draw(image)

        name = album["album"]
        if len(name) > text_cutoff_value:
            name = f"{name[:text_cutoff_value]}..."

        draw.text((col_pos, row_pos + increment_size), name, font=font, fill="white")

        col_pos += 200
        if col_pos > image_width - increment_size:
            row_pos += increment_size + 50
            col_pos = 0 

    row_pos += increment_size + 50
    col_pos = 0

    """B TIER"""
    if col_pos == 0:
        draw = ImageDraw.Draw(image)
        draw_tier_label(draw, col_pos, row_pos, "B Tier", "yellow", "black")
        col_pos += increment_size

    for album in data["b_tier"]:
        try:
            response = requests.get(album["cover_art"], timeout=8)
            response.raise_for_status()
            cover_art = Image.open(BytesIO(response.content))
        except Exception:
            cover_art = Image.new("RGB", (increment_size, increment_size), "gray")
        cover_art = cover_art.resize((increment_size, increment_size))
        image.paste(cover_art, (col_pos, row_pos))
        draw = ImageDraw.Draw(image)

        name = album["album"]
        if len(name) > text_cutoff_value:
            name = f"{name[:text_cutoff_value]}..."

        draw.text((col_pos, row_pos + increment_size), name, font=font, fill="white")
        col_pos += 200
        if col_pos > image_width - increment_size:
            # add a new row
            row_pos += increment_size + 50
            col_pos = 0

    row_pos += increment_size + 50
    col_pos = 0

    """C TIER"""
    if col_pos == 0:
        draw = ImageDraw.Draw(image)
        draw_tier_label(draw, col_pos, row_pos, "C Tier", "green", "black")
        col_pos += increment_size

    for album in data["c_tier"]:
        try:
            response = requests.get(album["cover_art"], timeout=8)
            response.raise_for_status()
            cover_art = Image.open(BytesIO(response.content))
        except Exception:
            cover_art = Image.new("RGB", (increment_size, increment_size), "gray")
        cover_art = cover_art.resize((increment_size, increment_size))
        image.paste(cover_art, (col_pos, row_pos))
        draw = ImageDraw.Draw(image)

        name = album["album"]
        if len(name) > text_cutoff_value:
            name = f"{name[:text_cutoff_value]}..."

        draw.text((col_pos, row_pos + increment_size), name, font=font, fill="white")

        col_pos += 200
        if col_pos > image_width - increment_size:
            row_pos += increment_size + 50
            col_pos = 0

    row_pos += increment_size + 50
    col_pos = 0


    """D TIER"""
    if col_pos == 0:
        draw = ImageDraw.Draw(image)
        draw_tier_label(draw, col_pos, row_pos, "D Tier", "blue", "black")
        col_pos += increment_size

    for album in data["d_tier"]:
        try:
            response = requests.get(album["cover_art"], timeout=8)
            response.raise_for_status()
            cover_art = Image.open(BytesIO(response.content))
        except Exception:
            cover_art = Image.new("RGB", (increment_size, increment_size), "gray")
        cover_art = cover_art.resize((increment_size, increment_size))
        image.paste(cover_art, (col_pos, row_pos))        
        draw = ImageDraw.Draw(image)

        name = album["album"]
        if len(name) > text_cutoff_value:
            name = f"{name[:text_cutoff_value]}..."

        draw.text((col_pos, row_pos + increment_size), name, font=font, fill="white")

        col_pos += 200
        if col_pos > image_width - increment_size:
            # add a new row
            row_pos += increment_size + 50
            col_pos = 0

    row_pos += increment_size + 50
    col_pos = 0


    """E TIER"""
    if col_pos == 0:
        draw = ImageDraw.Draw(image)
        draw_tier_label(draw, col_pos, row_pos, "E Tier", "pink", "black")
        col_pos += increment_size

    for album in data["e_tier"]:

        try:
            response = requests.get(album["cover_art"], timeout=8)
            response.raise_for_status()
            cover_art = Image.open(BytesIO(response.content))
        except Exception:
            cover_art = Image.new("RGB", (increment_size, increment_size), "gray")
        cover_art = cover_art.resize((increment_size, increment_size))    
        image.paste(cover_art, (col_pos, row_pos))
        draw = ImageDraw.Draw(image)
        name = album["album"]
        if len(name) > text_cutoff_value:
            name = f"{name[:text_cutoff_value]}..."

        draw.text((col_pos, row_pos + increment_size), name, font=font, fill="white")
        col_pos += 200
        if col_pos > image_width - increment_size:
            row_pos += increment_size + 50
            col_pos = 0

    row_pos += increment_size + 50
    col_pos = 0

    image = image.crop((0, 0, image_width, row_pos))

    image.save(f"{file_name}")
