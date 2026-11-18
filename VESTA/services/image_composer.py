
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps


# -----------------------------------------
# PATHS AND DESIGN SETTINGS
# -----------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

CANVAS_COLOUR = "#F1E9DC"
CARD_COLOUR = "#FAF7F1"
OXBLOOD = "#641F30"
GOLD = "#B39460"
CHARCOAL = "#292629"

IMAGE_WIDTH = 1600
CARD_WIDTH = 440
CARD_HEIGHT = 520
CARD_GAP = 35
MARGIN = 80
HEADER_HEIGHT = 180


# -----------------------------------------
# FONT LOADING
# -----------------------------------------

def load_font(size, bold=False):

    font_paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
        if bold
        else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]

    for font_path in font_paths:
        if Path(font_path).exists():
            return ImageFont.truetype(font_path, size)

    return ImageFont.load_default()


# -----------------------------------------
# IMAGE PATH RESOLUTION
# -----------------------------------------

def resolve_image_path(image_path):

    if not image_path:
        return None

    path = Path(image_path)

    if path.is_absolute() and path.exists():
        return path

    possible_paths = [
        BASE_DIR / path,
        BASE_DIR / "assets" / "clothing" / path.name,
    ]

    for possible_path in possible_paths:
        if possible_path.exists():
            return possible_path

    return None


# -----------------------------------------
# LOAD GARMENT PHOTOGRAPHS
# -----------------------------------------

def load_garment_image(item):

    image_path = resolve_image_path(item.image_path)

    if image_path is None:
        return None

    try:
        image = Image.open(image_path)
        image = ImageOps.exif_transpose(image)
        image = image.convert("RGBA")

        return image

    except (OSError, ValueError):
        return None


# -----------------------------------------
# CREATE FLAT-LAY MOCKUP
# -----------------------------------------

def compose_flat_lay(items):

    if not items:
        raise ValueError("No garments were selected.")

    loaded_items = []
    missing_items = []

    for item in items:

        image = load_garment_image(item)

        if image is None:
            missing_items.append(item.name)
            continue

        loaded_items.append((item, image))

    if not loaded_items:
        raise ValueError(
            "None of the selected garments have usable photographs."
        )

    columns = 3

    rows = (
        len(loaded_items) + columns - 1
    ) // columns

    canvas_height = (
        HEADER_HEIGHT
        + MARGIN
        + rows * CARD_HEIGHT
        + (rows - 1) * CARD_GAP
        + MARGIN
    )

    canvas = Image.new(
        "RGB",
        (IMAGE_WIDTH, canvas_height),
        CANVAS_COLOUR,
    )

    draw = ImageDraw.Draw(canvas)

    # ---------------------------------
    # HEADER
    # ---------------------------------

    title_font = load_font(54, bold=True)
    subtitle_font = load_font(22)

    draw.text(
        (MARGIN, 45),
        "V E S T A",
        fill=OXBLOOD,
        font=title_font,
    )

    draw.text(
        (MARGIN, 115),
        "YOUR WARDROBE, YOUR STYLE",
        fill=CHARCOAL,
        font=subtitle_font,
    )

    draw.line(
        (
            MARGIN,
            160,
            IMAGE_WIDTH - MARGIN,
            160,
        ),
        fill=GOLD,
        width=3,
    )

    # ---------------------------------
    # GARMENT CARDS
    # ---------------------------------

    category_font = load_font(18, bold=True)
    name_font = load_font(23)

    for index, (item, garment_image) in enumerate(loaded_items):

        row = index // columns
        column = index % columns

        x = MARGIN + column * (CARD_WIDTH + CARD_GAP)
        y = HEADER_HEIGHT + row * (CARD_HEIGHT + CARD_GAP)

        # Card background

        draw.rounded_rectangle(
            (
                x,
                y,
                x + CARD_WIDTH,
                y + CARD_HEIGHT,
            ),
            radius=18,
            fill=CARD_COLOUR,
        )

        # Garment photograph

        image_area_width = CARD_WIDTH - 50
        image_area_height = 390

        fitted_image = ImageOps.contain(
            garment_image,
            (image_area_width, image_area_height),
        )

        image_x = x + (CARD_WIDTH - fitted_image.width) // 2
        image_y = y + 15 + (
            image_area_height - fitted_image.height
        ) // 2

        canvas.paste(
            fitted_image,
            (image_x, image_y),
            fitted_image,
        )

        # Category

        draw.text(
            (x + 25, y + 420),
            str(item.category).upper(),
            fill=OXBLOOD,
            font=category_font,
        )

        # Garment name

        garment_name = str(item.name)

        if len(garment_name) > 32:
            garment_name = garment_name[:29] + "..."

        draw.text(
            (x + 25, y + 452),
            garment_name,
            fill=CHARCOAL,
            font=name_font,
        )

        # Decorative gold line

        draw.line(
            (
                x + 25,
                y + 495,
                x + 100,
                y + 495,
            ),
            fill=GOLD,
            width=3,
        )

    return canvas, missing_items
