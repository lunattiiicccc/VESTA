
from itertools import product

from engine.compatibility import is_valid_outfit
from engine.filtering import (
    filter_by_temperature,
    filter_by_weather,
    filter_by_season,
)
from engine.scoring import score_outfit
from engine.explanations import explain_outfit


def outfits_are_too_similar(outfit_a, outfit_b):
    """Check whether two outfits share too many garments."""

    ids_a = {item.id for item in outfit_a["items"]}
    ids_b = {item.id for item in outfit_b["items"]}

    shared_items = len(ids_a.intersection(ids_b))
    smaller_outfit = min(len(ids_a), len(ids_b))

    if smaller_outfit == 0:
        return False

    return shared_items / smaller_outfit > 0.5


def select_diverse_outfits(recommendations, limit):
    """Select high-scoring outfits while encouraging variety."""

    selected = []

    for recommendation in recommendations:
        too_similar = any(
            outfits_are_too_similar(recommendation, existing)
            for existing in selected
        )

        if not too_similar:
            selected.append(recommendation)

        if len(selected) == limit:
            return selected

    for recommendation in recommendations:
        if recommendation not in selected:
            selected.append(recommendation)

        if len(selected) == limit:
            break

    return selected


def generate_outfits(
    items,
    temperature=None,
    weather=None,
    season=None,
    formality=None,
    limit=3,
):
    """Generate and rank complete outfits with optional styling additions."""

    # ---------------------------------
    # FILTER WARDROBE
    # ---------------------------------

    suitable_items = items

    if temperature is not None:
        suitable_items = filter_by_temperature(
            suitable_items, temperature
        )

    if weather:
        suitable_items = filter_by_weather(
            suitable_items, weather
        )

    if season:
        suitable_items = filter_by_season(
            suitable_items, season
        )

    # ---------------------------------
    # SEPARATE GARMENT CATEGORIES
    # ---------------------------------

    tops = [
        item for item in suitable_items
        if item.category == "Top"
    ]

    bottoms = [
        item for item in suitable_items
        if item.category == "Bottom"
    ]

    dresses = [
        item for item in suitable_items
        if item.category == "Dress"
    ]

    jumpsuits = [
        item for item in suitable_items
        if item.category == "Jumpsuit"
    ]

    footwear = [
        item for item in suitable_items
        if item.category == "Footwear"
    ]

    outerwear = [
        item for item in suitable_items
        if item.category == "Outerwear"
    ]

    accessories = [
        item for item in suitable_items
        if item.category == "Accessory"
    ]

    # ---------------------------------
    # CREATE BASE OUTFITS
    # ---------------------------------

    base_outfits = []

    # Top + Bottom + Footwear
    for top, bottom, shoes in product(
        tops, bottoms, footwear
    ):
        base_outfits.append([top, bottom, shoes])

    # Dress + Footwear
    for dress, shoes in product(dresses, footwear):
        base_outfits.append([dress, shoes])

    # Jumpsuit + Footwear
    for jumpsuit, shoes in product(jumpsuits, footwear):
        base_outfits.append([jumpsuit, shoes])

    # ---------------------------------
    # ADD OPTIONAL STYLING
    # ---------------------------------

    combinations = []

    optional_outerwear = [None] + outerwear
    optional_accessories = [None] + accessories

    for base_outfit in base_outfits:

        for coat, accessory in product(
            optional_outerwear,
            optional_accessories,
        ):

            outfit = base_outfit.copy()

            if coat is not None:
                outfit.append(coat)

            if accessory is not None:
                outfit.append(accessory)

            combinations.append(outfit)

    # ---------------------------------
    # SCORE AND EXPLAIN OUTFITS
    # ---------------------------------

    recommendations = []

    for outfit in combinations:

        if not is_valid_outfit(outfit):
            continue

        score = score_outfit(
            outfit,
            temperature=temperature,
            weather=weather,
            formality=formality,
        )

        explanation = explain_outfit(
            outfit,
            score,
            temperature=temperature,
            weather=weather,
            formality=formality,
        )

        recommendations.append({
            "items": outfit,
            "score": score["total"],
            "breakdown": score["breakdown"],
            "explanation": explanation,
        })

    # ---------------------------------
    # RANK AND SELECT
    # ---------------------------------

    recommendations.sort(
        key=lambda outfit: outfit["score"],
        reverse=True,
    )

    return select_diverse_outfits(
        recommendations,
        limit,
    )
