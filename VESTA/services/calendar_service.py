
from datetime import date

from sqlalchemy.orm import Session, joinedload

from database.models import CalendarEvent, ClothingItem


# -----------------------------------------
# ADD CALENDAR EVENT
# -----------------------------------------

def add_calendar_event(
    db: Session,
    event_date: date,
    items: list,
    occasion: str = None,
    notes: str = None,
):
    """Save a planned outfit using garments from this session."""

    # Retrieve garment IDs rather than attaching objects
    # that may belong to another database session.

    item_ids = list({
        item.id for item in items
        if item.id is not None
    })

    session_items = (
        db.query(ClothingItem)
        .filter(ClothingItem.id.in_(item_ids))
        .all()
    ) if item_ids else []

    if len(session_items) != len(item_ids):
        raise ValueError(
            "One or more selected garments could not be found."
        )

    event = CalendarEvent(
        event_date=event_date,
        occasion=occasion,
        notes=notes,
        items=session_items,
    )

    try:
        db.add(event)
        db.commit()
        db.refresh(event)

        return event

    except Exception:
        db.rollback()
        raise


# -----------------------------------------
# GET CALENDAR EVENTS
# -----------------------------------------

def get_calendar_events(
    db: Session,
    start_date: date = None,
    end_date: date = None,
):
    """Retrieve calendar events, optionally within a date range."""

    query = (
        db.query(CalendarEvent)
        .options(joinedload(CalendarEvent.items))
    )

    if start_date is not None:
        query = query.filter(
            CalendarEvent.event_date >= start_date
        )

    if end_date is not None:
        query = query.filter(
            CalendarEvent.event_date <= end_date
        )

    return (
        query
        .order_by(CalendarEvent.event_date.asc())
        .all()
    )


# -----------------------------------------
# GET SINGLE CALENDAR EVENT
# -----------------------------------------

def get_calendar_event_by_id(db: Session, event_id: int):
    """Retrieve one calendar event by its ID."""

    return (
        db.query(CalendarEvent)
        .options(joinedload(CalendarEvent.items))
        .filter(CalendarEvent.id == event_id)
        .first()
    )


# -----------------------------------------
# DELETE CALENDAR EVENT
# -----------------------------------------

def delete_calendar_event(db: Session, event_id: int):
    """Delete a planned outfit from the calendar."""

    event = db.query(CalendarEvent).filter(
        CalendarEvent.id == event_id
    ).first()

    if event is None:
        return False

    try:
        db.delete(event)
        db.commit()

        return True

    except Exception:
        db.rollback()
        raise


# -----------------------------------------
# GET EVENTS FOR A SPECIFIC DATE
# -----------------------------------------

def get_events_for_date(db: Session, event_date: date):
    """Retrieve all planned outfits for a particular date."""

    return (
        db.query(CalendarEvent)
        .options(joinedload(CalendarEvent.items))
        .filter(CalendarEvent.event_date == event_date)
        .order_by(CalendarEvent.id.asc())
        .all()
    )
