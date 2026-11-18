
from sqlalchemy.orm import Session, joinedload

from database.models import SavedOutfit, ClothingItem


# -----------------------------------------
# CREATE SAVED OUTFIT
# -----------------------------------------

def add_saved_outfit(db: Session, name, items, description=None):
    """Create a saved outfit using existing wardrobe garments."""

    name = (name or "").strip()

    if not name:
        raise ValueError("Please provide a name for the outfit.")

    item_ids = list({
        item.id for item in items
        if item.id is not None
    })

    if not item_ids:
        raise ValueError("Please select at least one garment.")

    session_items = (
        db.query(ClothingItem)
        .filter(ClothingItem.id.in_(item_ids))
        .all()
    )

    if len(session_items) != len(item_ids):
        raise ValueError("One or more selected garments could not be found.")

    outfit = SavedOutfit(
        name=name,
        description=description,
        items=session_items
    )

    try:
        db.add(outfit)
        db.commit()
        db.refresh(outfit)
        return outfit

    except Exception:
        db.rollback()
        raise


# -----------------------------------------
# GET ALL SAVED OUTFITS
# -----------------------------------------

def get_all_saved_outfits(db: Session):
    """Retrieve all saved outfits and their garments."""

    return (
        db.query(SavedOutfit)
        .options(joinedload(SavedOutfit.items))
        .order_by(SavedOutfit.created_at.desc())
        .all()
    )


# -----------------------------------------
# GET SAVED OUTFIT BY ID
# -----------------------------------------

def get_saved_outfit_by_id(db: Session, outfit_id):
    """Retrieve one saved outfit."""

    return (
        db.query(SavedOutfit)
        .options(joinedload(SavedOutfit.items))
        .filter(SavedOutfit.id == outfit_id)
        .first()
    )


# -----------------------------------------
# UPDATE SAVED OUTFIT
# -----------------------------------------

def update_saved_outfit(
    db: Session,
    outfit_id,
    name,
    items=None,
    description=None
):
    """Update a saved outfit's details and garments."""

    outfit = get_saved_outfit_by_id(db, outfit_id)

    if outfit is None:
        return None

    name = (name or "").strip()

    if not name:
        raise ValueError("Please provide a name for the outfit.")

    try:
        outfit.name = name
        outfit.description = description

        if items is not None:
            item_ids = list({
                item.id for item in items
                if item.id is not None
            })

            if not item_ids:
                raise ValueError("Please select at least one garment.")

            session_items = (
                db.query(ClothingItem)
                .filter(ClothingItem.id.in_(item_ids))
                .all()
            )

            if len(session_items) != len(item_ids):
                raise ValueError(
                    "One or more selected garments could not be found."
                )

            outfit.items = session_items

        db.commit()
        db.refresh(outfit)

        return outfit

    except Exception:
        db.rollback()
        raise


# -----------------------------------------
# DELETE SAVED OUTFIT
# -----------------------------------------

def delete_saved_outfit(db: Session, outfit_id):
    """Delete a saved outfit without deleting its garments."""

    outfit = (
        db.query(SavedOutfit)
        .filter(SavedOutfit.id == outfit_id)
        .first()
    )

    if outfit is None:
        return False

    try:
        db.delete(outfit)
        db.commit()
        return True

    except Exception:
        db.rollback()
        raise
