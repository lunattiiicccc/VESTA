
from pathlib import Path
from uuid import uuid4

from PIL import Image, UnidentifiedImageError
from sqlalchemy import func
from sqlalchemy.orm import Session

from database.models import ClothingItem, Tag


BASE_DIR = Path(__file__).resolve().parent.parent
IMAGE_DIR = BASE_DIR / "assets" / "clothing"

IMAGE_DIR.mkdir(parents=True, exist_ok=True)


def save_clothing_image(uploaded_file):
    """Validate and save an uploaded clothing photograph."""

    if uploaded_file is None:
        return None

    try:
        image = Image.open(uploaded_file)
        image.verify()

        # Reopen after verification and convert to a standard format
        uploaded_file.seek(0)
        image = Image.open(uploaded_file).convert("RGB")

        filename = f"{uuid4().hex}.jpg"
        destination = IMAGE_DIR / filename

        image.save(destination, "JPEG", quality=90)

        return f"assets/clothing/{filename}"

    except (UnidentifiedImageError, OSError) as error:
        raise ValueError("Please upload a valid image file.") from error


def get_all_clothing(db: Session):
    """Retrieve all clothing items."""

    return (
        db.query(ClothingItem)
        .order_by(ClothingItem.created_at.desc())
        .all()
    )


def get_clothing_by_id(db: Session, item_id: int):
    """Retrieve one garment by its ID."""

    return db.query(ClothingItem).filter(
        ClothingItem.id == item_id
    ).first()


def get_or_create_tags(db: Session, tag_names: list[str]):
    """Find existing tags or create new ones."""

    result = []

    for name in tag_names:
        name = name.strip()

        if not name:
            continue

        tag = db.query(Tag).filter(
            func.lower(Tag.name) == name.lower()
        ).first()

        if tag is None:
            tag = Tag(name=name)
            db.add(tag)
            db.flush()

        result.append(tag)

    return result


def add_clothing(
    db: Session,
    name: str,
    category: str,
    subcategory: str,
    primary_colour: str,
    secondary_colour: str,
    material: str,
    fit: str,
    seasons: list[str],
    min_temperature: float,
    max_temperature: float,
    weather_suitability: list[str],
    formality: str,
    notes: str,
    tags: list[str],
    image_path: str | None = None,
):
    """Create a new clothing item."""

    item = ClothingItem(
        name=name.strip(),
        category=category,
        subcategory=subcategory or None,
        primary_colour=primary_colour,
        secondary_colour=secondary_colour or None,
        material=material or None,
        fit=fit or None,
        seasons=", ".join(seasons),
        min_temperature=min_temperature,
        max_temperature=max_temperature,
        weather_suitability=", ".join(weather_suitability),
        formality=formality,
        notes=notes or None,
        image_path=image_path,
        is_demo=False,
    )

    item.tags = get_or_create_tags(db, tags)

    db.add(item)
    db.commit()
    db.refresh(item)

    return item


def delete_clothing(db: Session, item_id: int):
    """Delete a clothing item and its stored image."""

    item = get_clothing_by_id(db, item_id)

    if item is None:
        return False

    image_path = item.image_path

    db.delete(item)
    db.commit()

    if image_path:
        full_path = (BASE_DIR / image_path).resolve()

        # Only delete files inside the clothing image directory
        if full_path.is_relative_to(IMAGE_DIR.resolve()):
            full_path.unlink(missing_ok=True)

    return True


def update_clothing(
    db: Session,
    item_id: int,
    name: str,
    category: str,
    subcategory: str,
    primary_colour: str,
    secondary_colour: str,
    material: str,
    fit: str,
    seasons: list[str],
    min_temperature: float,
    max_temperature: float,
    weather_suitability: list[str],
    formality: str,
    notes: str,
    tags: list[str],
    image_path: str | None = None,
):
    """Update an existing clothing item."""

    item = get_clothing_by_id(db, item_id)

    if item is None:
        return None

    item.name = name.strip()
    item.category = category
    item.subcategory = subcategory or None
    item.primary_colour = primary_colour
    item.secondary_colour = secondary_colour or None
    item.material = material or None
    item.fit = fit or None
    item.seasons = ", ".join(seasons)
    item.min_temperature = min_temperature
    item.max_temperature = max_temperature
    item.weather_suitability = ", ".join(weather_suitability)
    item.formality = formality
    item.notes = notes or None

    # Replace tags with the newly selected tags
    item.tags = get_or_create_tags(db, tags)

    # Only replace the photograph if a new one was uploaded
    if image_path is not None:
        old_image_path = item.image_path
        item.image_path = image_path

        db.commit()

        # Remove the previous photograph after a successful update
        if old_image_path:
            full_path = (BASE_DIR / old_image_path).resolve()

            if full_path.is_relative_to(IMAGE_DIR.resolve()):
                full_path.unlink(missing_ok=True)
    else:
        db.commit()

    db.refresh(item)

    return item

