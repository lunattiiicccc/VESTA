
def explain_outfit(
    outfit,
    score_breakdown,
    temperature=None,
    weather=None,
    formality=None,
):
    """Generate a readable explanation for an outfit recommendation."""

    explanations = []

    breakdown = score_breakdown["breakdown"]

    # ---------------------------------
    # WEATHER
    # ---------------------------------

    if breakdown["weather"] >= 85:
        explanations.append(
            "The garments are well suited to the current weather."
        )

    elif breakdown["weather"] >= 60:
        explanations.append(
            "The outfit is reasonably suited to the weather."
        )

    else:
        explanations.append(
            "Some garments may be less suitable for the current weather."
        )

    # ---------------------------------
    # COLOUR
    # ---------------------------------

    if breakdown["colour"] >= 90:
        explanations.append(
            "The colours coordinate particularly well."
        )

    elif breakdown["colour"] >= 75:
        explanations.append(
            "The colour combination creates a balanced look."
        )

    # ---------------------------------
    # OCCASION
    # ---------------------------------

    if breakdown["occasion"] >= 90:
        explanations.append(
            "The garments are a strong match for your chosen occasion."
        )

    elif breakdown["occasion"] >= 70:
        explanations.append(
            "The outfit is reasonably appropriate for your chosen occasion."
        )

    # ---------------------------------
    # STYLE
    # ---------------------------------

    if breakdown["style"] >= 90:
        explanations.append(
            "The garments share complementary style tags."
        )

    # ---------------------------------
    # OUTFIT STRUCTURE
    # ---------------------------------

    categories = [item.category for item in outfit]

    if "Dress" in categories:
        explanations.append(
            "A dress creates a simple, complete outfit foundation."
        )

    elif "Jumpsuit" in categories:
        explanations.append(
            "A jumpsuit provides an easy one-piece outfit foundation."
        )

    elif "Top" in categories and "Bottom" in categories:
        explanations.append(
            "The top and bottom create a complete separates combination."
        )

    # ---------------------------------
    # OUTERWEAR
    # ---------------------------------

    outerwear_items = [
        item for item in outfit
        if item.category == "Outerwear"
    ]

    if outerwear_items:
        explanations.append(
            f"{outerwear_items[0].name} adds an extra layer to the outfit."
        )

    # ---------------------------------
    # ACCESSORIES
    # ---------------------------------

    accessory_items = [
        item for item in outfit
        if item.category == "Accessory"
    ]

    if accessory_items:
        explanations.append(
            f"{accessory_items[0].name} completes the look with an additional detail."
        )

    # ---------------------------------
    # WEATHER CONTEXT
    # ---------------------------------

    if temperature is not None:
        explanations.append(
            f"Selected for a temperature of approximately {temperature}°C."
        )

    if weather:
        explanations.append(
            f"Weather considered: {weather.lower()}."
        )

    # ---------------------------------
    # OCCASION CONTEXT
    # ---------------------------------

    if formality:
        explanations.append(
            f"Your selected occasion: {formality.lower()}."
        )

    return explanations
