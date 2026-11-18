
from engine.compatibility import is_valid_outfit


# ---------------------------------
# COLOUR GROUPS
# ---------------------------------

COLOUR_FAMILIES = {
    "neutral": [
        "Black", "White", "Grey", "Cream",
        "Beige", "Brown"
    ],
    "red": ["Red", "Burgundy"],
    "pink": ["Pink"],
    "purple": ["Purple"],
    "blue": ["Blue"],
    "green": ["Green"],
    "warm": ["Yellow", "Orange"],
    "mixed": ["Multicoloured", "Other"],
}


def get_colour_family(colour):
    """Find the general colour family of a garment."""

    for family, colours in COLOUR_FAMILIES.items():
        if colour in colours:
            return family

    return "unknown"


# ---------------------------------
# WEATHER SCORE
# ---------------------------------

def score_weather(outfit, temperature=None, weather=None):
    """Score how suitable an outfit is for the weather."""

    scores = []

    for item in outfit:
        score = 100

        if temperature is not None:
            minimum = item.min_temperature
            maximum = item.max_temperature

            if minimum is not None and temperature < minimum:
                score -= 50

            elif maximum is not None and temperature > maximum:
                score -= 50

        if weather:
            suitability = [
                value.strip().lower()
                for value in (item.weather_suitability or "").split(",")
            ]

            if suitability and "any" not in suitability:
                if weather.lower() not in suitability:
                    score -= 40

        scores.append(max(0, score))

    return sum(scores) / len(scores) if scores else 0


# ---------------------------------
# CLOTHING COMPATIBILITY SCORE
# ---------------------------------

def score_compatibility(outfit):
    """Score whether garments form a valid outfit."""

    return 100 if is_valid_outfit(outfit) else 0


# ---------------------------------
# OCCASION SCORE
# ---------------------------------

FORMALITY_LEVELS = [
    "Casual",
    "Smart Casual",
    "Business Casual",
    "Formal",
    "Evening",
]


def score_occasion(outfit, formality=None):
    """Score how well an outfit matches the requested occasion."""

    if not formality:
        return 70

    if formality not in FORMALITY_LEVELS:
        return 70

    requested_level = FORMALITY_LEVELS.index(formality)
    scores = []

    for item in outfit:
        if not item.formality:
            scores.append(70)
            continue

        if item.formality not in FORMALITY_LEVELS:
            scores.append(70)
            continue

        item_level = FORMALITY_LEVELS.index(item.formality)
        difference = abs(requested_level - item_level)

        score = max(0, 100 - (difference * 25))
        scores.append(score)

    return sum(scores) / len(scores) if scores else 0


# ---------------------------------
# COLOUR COORDINATION SCORE
# ---------------------------------

def score_colour(outfit):
    """Score how well the garment colours coordinate."""

    colours = [
        item.primary_colour
        for item in outfit
        if item.primary_colour
    ]

    if len(colours) < 2:
        return 70

    pair_scores = []

    for index, colour in enumerate(colours):
        for other_colour in colours[index + 1:]:
            family = get_colour_family(colour)
            other_family = get_colour_family(other_colour)

            if family == other_family:
                score = 100

            elif family == "neutral" or other_family == "neutral":
                score = 90

            elif "unknown" in [family, other_family]:
                score = 60

            else:
                score = 70

            pair_scores.append(score)

    return sum(pair_scores) / len(pair_scores)


# ---------------------------------
# STYLE COORDINATION SCORE
# ---------------------------------

def score_style(outfit):
    """Score shared style tags across garments."""

    garment_tags = [
        {tag.name.lower() for tag in item.tags}
        for item in outfit
    ]

    tagged_garments = [
        tags for tags in garment_tags if tags
    ]

    if len(tagged_garments) < 2:
        return 70

    shared_tags = set.intersection(*tagged_garments)

    if shared_tags:
        return 100

    return 70


# ---------------------------------
# TOTAL OUTFIT SCORE
# ---------------------------------

def score_outfit(
    outfit,
    temperature=None,
    weather=None,
    formality=None
):
    """Calculate the weighted score for a complete outfit."""

    breakdown = {
        "weather": score_weather(outfit, temperature, weather),
        "compatibility": score_compatibility(outfit),
        "occasion": score_occasion(outfit, formality),
        "colour": score_colour(outfit),
        "style": score_style(outfit),
    }

    total = (
        breakdown["weather"] * 0.30
        + breakdown["compatibility"] * 0.25
        + breakdown["occasion"] * 0.20
        + breakdown["colour"] * 0.15
        + breakdown["style"] * 0.10
    )

    return {
        "total": round(total, 2),
        "breakdown": {
            key: round(value, 2)
            for key, value in breakdown.items()
        }
    }
