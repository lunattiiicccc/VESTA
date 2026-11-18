
def can_form_outfit(top, bottom):
    """Check whether a top and bottom can form an outfit."""

    if top.category != "Top":
        return False

    if bottom.category != "Bottom":
        return False

    return True


def get_outfit_type(item):
    """Determine the basic structure of an outfit."""

    if item.category == "Dress":
        return "dress"

    if item.category == "Jumpsuit":
        return "jumpsuit"

    if item.category == "Top":
        return "separates"

    return None


def is_valid_outfit(outfit):
    """Check whether an outfit has a valid clothing structure."""

    categories = [item.category for item in outfit]

    has_footwear = "Footwear" in categories

    has_dress = "Dress" in categories
    has_jumpsuit = "Jumpsuit" in categories

    has_top = "Top" in categories
    has_bottom = "Bottom" in categories

    # Dresses and jumpsuits need footwear
    if has_dress or has_jumpsuit:
        return has_footwear

    # Separates need a top, bottom and footwear
    if has_top and has_bottom:
        return has_footwear

    return False

