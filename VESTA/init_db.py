
from database.connection import engine, Base
from database.models import (
    ClothingItem,
    Tag,
    CalendarEvent,
    calendar_event_items,
)


def initialise_database():

    print("Initialising VESTA database...")

    Base.metadata.create_all(bind=engine)

    print("Database created successfully!")
    print(f"Database location: {engine.url.database}")


if __name__ == "__main__":
    initialise_database()
