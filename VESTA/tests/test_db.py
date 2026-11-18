
from database.connection import SessionLocal
from database.models import ClothingItem


def test_database_connection():

    db = SessionLocal()

    try:
        items = db.query(ClothingItem).all()

        assert isinstance(items, list)

        print("Database connection successful!")
        print(f"Current clothing items: {len(items)}")

    finally:
        db.close()


if __name__ == "__main__":
    test_database_connection()
