from types import SimpleNamespace

from engine.generator import generate_outfits


def make_item(item_id, name, category, colour, formality="Casual"):
    return SimpleNamespace(
        id=item_id,
        name=name,
        category=category,
        primary_colour=colour,
        min_temperature=None,
        max_temperature=None,
        weather_suitability="Any",
        seasons="Spring,Summer,Autumn,Winter",
        formality=formality,
        tags=[],
    )


def test_generate_outfits():
    wardrobe = [
    make_item(1, "White T-shirt", "Top", "White"),
    make_item(2, "Black blouse", "Top", "Black"),
    make_item(3, "Blue jeans", "Bottom", "Blue"),
    make_item(4, "Black trousers", "Bottom", "Black"),
    make_item(5, "White trainers", "Footwear", "White"),
    make_item(6, "Black boots", "Footwear", "Black"),
    make_item(7, "Red dress", "Dress", "Red"),
    ]

    outfits = generate_outfits(wardrobe)

    assert len(outfits) > 0
    assert len(outfits) <= 3

    for outfit in outfits:
        assert outfit["score"] >= 0
        assert outfit["score"] <= 100
        assert len(outfit["items"]) >= 2
        assert outfit["explanation"]


if __name__ == "__main__":
    test_generate_outfits()
    print("Outfit generator test passed!")