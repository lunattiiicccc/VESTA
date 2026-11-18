
def filter_by_temperature(items, temperature):
    """Remove garments unsuitable for the current temperature."""

    suitable_items = []

    for item in items:
        minimum = item.min_temperature
        maximum = item.max_temperature

        if minimum is not None and temperature < minimum:
            continue

        if maximum is not None and temperature > maximum:
            continue

        suitable_items.append(item)

    return suitable_items


def filter_by_weather(items, weather):
    """Filter garments by their weather suitability."""

    if not weather:
        return items

    suitable_items = []

    for item in items:
        suitability = [
            condition.strip().lower()
            for condition in (item.weather_suitability or "").split(",")
        ]

        if not suitability or "any" in suitability:
            suitable_items.append(item)

        elif weather.lower() in suitability:
            suitable_items.append(item)

    return suitable_items


def filter_by_season(items, season):
    """Filter garments by their suitable seasons."""

    if not season:
        return items

    suitable_items = []

    for item in items:
        seasons = [
            value.strip().lower()
            for value in (item.seasons or "").split(",")
        ]

        if season.lower() in seasons:
            suitable_items.append(item)

    return suitable_items


def filter_by_formality(items, formality):
    """Filter garments by formality."""

    if not formality:
        return items

    return [
        item for item in items
        if item.formality == formality
    ]
