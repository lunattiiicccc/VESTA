
from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Boolean,
    DateTime,
    Date,
    Table,
    ForeignKey,
)
from sqlalchemy.orm import relationship

from database.connection import Base


# -----------------------------------------
# CLOTHING AND TAG RELATIONSHIP
# -----------------------------------------

clothing_tags = Table(
    "clothing_tags",
    Base.metadata,

    Column("clothing_id", Integer, ForeignKey("clothing_items.id"), primary_key=True),
    Column("tag_id", Integer, ForeignKey("tags.id"), primary_key=True)
)


# -----------------------------------------
# CALENDAR AND CLOTHING RELATIONSHIP
# -----------------------------------------

calendar_event_items = Table(
    "calendar_event_items",
    Base.metadata,

    Column("event_id", Integer, ForeignKey("calendar_events.id"), primary_key=True),
    Column("clothing_id", Integer, ForeignKey("clothing_items.id"), primary_key=True)
)


# -----------------------------------------
# SAVED OUTFIT AND CLOTHING RELATIONSHIP
# -----------------------------------------

saved_outfit_items = Table(
    "saved_outfit_items",
    Base.metadata,

    Column("outfit_id", Integer, ForeignKey("saved_outfits.id"), primary_key=True),
    Column("clothing_id", Integer, ForeignKey("clothing_items.id"), primary_key=True)
)


# -----------------------------------------
# CLOTHING ITEM
# -----------------------------------------

class ClothingItem(Base):

    __tablename__ = "clothing_items"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False)
    category = Column(String, nullable=False)
    subcategory = Column(String, nullable=True)

    primary_colour = Column(String, nullable=False)
    secondary_colour = Column(String, nullable=True)

    material = Column(String, nullable=True)
    fit = Column(String, nullable=True)

    seasons = Column(String, nullable=True)
    min_temperature = Column(Float, nullable=True)
    max_temperature = Column(Float, nullable=True)
    weather_suitability = Column(String, nullable=True)

    formality = Column(String, nullable=True)
    notes = Column(String, nullable=True)

    image_path = Column(String, nullable=True)

    is_demo = Column(Boolean, default=False)

    created_at = Column(DateTime, default=datetime.utcnow)

    tags = relationship(
        "Tag",
        secondary=clothing_tags,
        back_populates="clothing_items"
    )

    calendar_events = relationship(
        "CalendarEvent",
        secondary=calendar_event_items,
        back_populates="items"
    )

    saved_outfits = relationship(
        "SavedOutfit",
        secondary=saved_outfit_items,
        back_populates="items"
    )


# -----------------------------------------
# TAG
# -----------------------------------------

class Tag(Base):

    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, unique=True, nullable=False)

    clothing_items = relationship(
        "ClothingItem",
        secondary=clothing_tags,
        back_populates="tags"
    )


# -----------------------------------------
# CALENDAR EVENT
# -----------------------------------------

class CalendarEvent(Base):

    __tablename__ = "calendar_events"

    id = Column(Integer, primary_key=True, index=True)

    event_date = Column(Date, nullable=False, index=True)

    occasion = Column(String, nullable=True)

    notes = Column(String, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)

    items = relationship(
        "ClothingItem",
        secondary=calendar_event_items,
        back_populates="calendar_events"
    )


# -----------------------------------------
# SAVED OUTFIT
# -----------------------------------------

class SavedOutfit(Base):

    __tablename__ = "saved_outfits"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False)

    description = Column(String, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)

    items = relationship(
        "ClothingItem",
        secondary=saved_outfit_items,
        back_populates="saved_outfits"
    )
