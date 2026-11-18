
import streamlit as st
from pathlib import Path
from collections import Counter

from database.connection import SessionLocal
from services.clothing_service import (
    add_clothing,
    update_clothing,
    delete_clothing,
    get_all_clothing,
    save_clothing_image,
)


# -----------------------------------------
# SUBCATEGORY OPTIONS
# -----------------------------------------

SUBCATEGORY_OPTIONS = {
    "Top": [
        "T-shirt", "Blouse", "Shirt", "Jumper",
        "Knitwear", "Vest Top", "Other",
    ],
    "Bottom": [
        "Jeans", "Trousers", "Leggings", "Skirt",
        "Shorts", "Other",
    ],
    "Dress": [
        "Mini Dress", "Midi Dress", "Maxi Dress", "Other",
    ],
    "Jumpsuit": [
        "Jumpsuit", "Playsuit", "Other",
    ],
    "Outerwear": [
        "Coat", "Jacket", "Blazer", "Cardigan",
        "Gilet", "Other",
    ],
    "Footwear": [
        "Trainers", "Boots", "Heels", "Flats",
        "Sandals", "Loafers", "Other",
    ],
    "Accessory": [
        "Bag", "Belt", "Scarf", "Jewellery",
        "Hat", "Gloves", "Other",
    ],
}

CATEGORY_OPTIONS = list(SUBCATEGORY_OPTIONS.keys())

COLOUR_OPTIONS = [
    "Black", "White", "Grey", "Cream",
    "Beige", "Brown", "Red", "Burgundy",
    "Pink", "Purple", "Blue", "Green",
    "Yellow", "Orange", "Multicoloured", "Other",
]

FIT_OPTIONS = [
    "Regular", "Relaxed", "Oversized",
    "Slim", "Fitted", "Structured", "Other",
]

SEASON_OPTIONS = ["Spring", "Summer", "Autumn", "Winter"]

WEATHER_OPTIONS = [
    "Sunny", "Cloudy", "Rainy", "Windy",
    "Snowy", "Cold", "Warm", "Any",
]

FORMALITY_OPTIONS = [
    "Casual", "Smart Casual", "Business Casual",
    "Formal", "Evening",
]


def get_subcategory_options(category, current_value=None):
    """Return subcategories while preserving existing custom values."""

    options = SUBCATEGORY_OPTIONS[category].copy()

    if current_value and current_value not in options:
        options.insert(-1, current_value)

    return options



def render_collection_overview(items):
    """Display a refined statistical overview of the personal wardrobe."""

    # Exclude sample garments from personal wardrobe statistics.
    personal_items = [
        item for item in items
        if not getattr(item, "is_demo", False)
    ]

    total = len(personal_items)

    category_counts = Counter(
        item.category for item in personal_items
        if item.category
    )

    colour_counts = Counter(
        item.primary_colour for item in personal_items
        if item.primary_colour
    )

    category_order = [
        ("Top", "Tops"),
        ("Bottom", "Bottoms"),
        ("Dress", "Dresses"),
        ("Jumpsuit", "Jumpsuits"),
        ("Outerwear", "Outerwear"),
        ("Footwear", "Footwear"),
        ("Accessory", "Accessories"),
    ]

    season_order = ["Spring", "Summer", "Autumn", "Winter"]

    seasonal_counts = {}

    for season in season_order:
        seasonal_counts[season] = sum(
            1 for item in personal_items
            if season.lower() in [
                value.strip().lower()
                for value in (item.seasons or "").split(",")
            ]
        )

    colour_swatches = {
        "Black": "#292629",
        "White": "#FFFFFF",
        "Grey": "#929292",
        "Cream": "#F1E9DC",
        "Beige": "#D6C2A5",
        "Brown": "#795548",
        "Red": "#B32635",
        "Burgundy": "#641F30",
        "Pink": "#D99AA8",
        "Purple": "#76518C",
        "Blue": "#557A9C",
        "Green": "#637B58",
        "Yellow": "#E5C45B",
        "Orange": "#D98545",
        "Multicoloured": "linear-gradient(90deg, #B32635, #E5C45B, #557A9C)",
        "Other": "#A69B91",
    }

    st.markdown("""
    <style>
    .collection-overview {
        background: #FFFFFF;
        border: 1px solid #DCCFC1;
        border-radius: 5px;
        padding: 24px 28px;
        margin: 20px 0;
    }

    .overview-eyebrow {
        color: #B39460;
        font-family: 'Manrope', sans-serif;
        font-size: 10px;
        font-weight: 700;
        letter-spacing: 2px;
        text-transform: uppercase;
    }

    .overview-total {
        color: #641F30;
        font-family: 'Cormorant Garamond', serif;
        font-size: 48px;
        line-height: 1.1;
    }

    .overview-description {
        color: #71666A;
        font-family: 'EB Garamond', serif;
        font-size: 16px;
    }

    .overview-section-title {
        color: #641F30;
        font-family: 'Cormorant Garamond', serif;
        font-size: 25px;
        margin-bottom: 12px;
    }

    .overview-detail-label {
        color: #81747A;
        font-family: 'Manrope', sans-serif;
        font-size: 10px;
        letter-spacing: 1px;
        text-transform: uppercase;
    }

    .overview-divider {
        border-top: 1px solid #E5D9CC;
        margin: 22px 0;
    }

    .category-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 8px 0;
        border-bottom: 1px solid #F0E9E1;
    }

    .category-name {
        color: #292629;
        font-family: 'Source Sans 3', sans-serif;
        font-size: 14px;
    }

    .category-count {
        color: #641F30;
        font-family: 'Cormorant Garamond', serif;
        font-size: 20px;
        font-weight: 600;
    }

    .colour-row {
        display: flex;
        align-items: center;
        gap: 9px;
        padding: 7px 0;
    }

    .colour-swatch {
        width: 19px;
        height: 19px;
        border-radius: 50%;
        border: 1px solid #DCCFC1;
        flex-shrink: 0;
    }

    .colour-name {
        color: #292629;
        font-family: 'Source Sans 3', sans-serif;
        font-size: 13px;
        flex-grow: 1;
    }

    .colour-count {
        color: #641F30;
        font-family: 'Cormorant Garamond', serif;
        font-size: 18px;
    }

    .season-row {
        display: flex;
        justify-content: space-between;
        padding: 7px 0;
        color: #292629;
        font-family: 'Source Sans 3', sans-serif;
        font-size: 14px;
    }

    .season-count {
        color: #641F30;
        font-family: 'Cormorant Garamond', serif;
        font-size: 18px;
    }

    .overview-note {
        color: #81747A;
        font-family: 'Source Sans 3', sans-serif;
        font-size: 12px;
        margin-top: 8px;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown(
        '<div class="overview-eyebrow">YOUR COLLECTION</div>',
        unsafe_allow_html=True
    )

    # COLLECTION TOTAL
    col1, col2, col3 = st.columns([1, 1, 1])

    with col1:
        st.markdown(
            f"""
            <div class="overview-total">{total}</div>
            <div class="overview-description">Personal garments</div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            f"""
            <div class="overview-total">{len(category_counts)}</div>
            <div class="overview-description">Categories represented</div>
            """,
            unsafe_allow_html=True
        )

    with col3:
        st.markdown(
            f"""
            <div class="overview-total">{len(colour_counts)}</div>
            <div class="overview-description">Colours represented</div>
            """,
            unsafe_allow_html=True
        )

    st.markdown(
        '<div class="overview-divider"></div>',
        unsafe_allow_html=True
    )

    # CATEGORY AND COLOUR BREAKDOWN
    category_column, colour_column = st.columns(2)

    with category_column:
        st.markdown(
            '<div class="overview-section-title">By category</div>',
            unsafe_allow_html=True
        )

        for category, label in category_order:
            count = category_counts.get(category, 0)

            st.markdown(
                f"""
                <div class="category-row">
                    <span class="category-name">{label}</span>
                    <span class="category-count">{count}</span>
                </div>
                """,
                unsafe_allow_html=True
            )

    with colour_column:
        st.markdown(
            '<div class="overview-section-title">Your colour palette</div>',
            unsafe_allow_html=True
        )

        if colour_counts:
            for colour, count in colour_counts.most_common(7):
                swatch = colour_swatches.get(colour, "#A69B91")

                st.markdown(
                    f"""
                    <div class="colour-row">
                        <span class="colour-swatch"
                            style="background: {swatch};"></span>
                        <span class="colour-name">{colour}</span>
                        <span class="colour-count">{count}</span>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
        else:
            st.caption("Your colour palette will appear here as you add garments.")

    st.markdown(
        '<div class="overview-divider"></div>',
        unsafe_allow_html=True
    )

    # SEASONAL COVERAGE
    st.markdown(
        '<div class="overview-section-title">Seasonal coverage</div>',
        unsafe_allow_html=True
    )

    season_columns = st.columns(4)

    for index, season in enumerate(season_order):
        count = seasonal_counts[season]

        with season_columns[index]:
            st.markdown(
                f"""
                <div class="overview-detail-label">{season}</div>
                <div class="overview-total" style="font-size: 32px;">
                    {count}
                </div>
                <div class="overview-description">Garments</div>
                """,
                unsafe_allow_html=True
            )

            progress = count / total if total else 0
            st.progress(progress)

    st.markdown(
        '<div class="overview-note">Seasonal coverage is based on the seasons assigned to your garments. A garment can belong to multiple seasons.</div>',
        unsafe_allow_html=True
    )

    """Display a refined summary of the user's wardrobe."""

    total = len(items)
    personal_count = total

    category_counts = Counter(
        item.category for item in items if item.category
    )

    category_order = [
        ("Top", "Tops"),
        ("Bottom", "Bottoms"),
        ("Dress", "Dresses"),
        ("Jumpsuit", "Jumpsuits"),
        ("Outerwear", "Outerwear"),
        ("Footwear", "Footwear"),
        ("Accessory", "Accessories"),
    ]

    st.markdown("""
    <style>
    .collection-overview {
        background: #FFFFFF;
        border: 1px solid #DCCFC1;
        border-radius: 5px;
        padding: 24px 28px;
        margin: 20px 0;
    }

    .overview-eyebrow {
        color: #B39460;
        font-family: 'Manrope', sans-serif;
        font-size: 10px;
        font-weight: 700;
        letter-spacing: 2px;
        text-transform: uppercase;
    }

    .overview-total {
        color: #641F30;
        font-family: 'Cormorant Garamond', serif;
        font-size: 48px;
        line-height: 1.1;
        margin-top: 5px;
    }

    .overview-description {
        color: #71666A;
        font-family: 'EB Garamond', serif;
        font-size: 16px;
    }

    .overview-divider {
        border-top: 1px solid #E5D9CC;
        margin: 20px 0;
    }

    .overview-detail-label {
        color: #81747A;
        font-family: 'Manrope', sans-serif;
        font-size: 10px;
        letter-spacing: 1px;
        text-transform: uppercase;
    }

    .overview-detail-value {
        color: #641F30;
        font-family: 'Cormorant Garamond', serif;
        font-size: 25px;
    }

    .category-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 9px 0;
        border-bottom: 1px solid #F0E9E1;
    }

    .category-name {
        color: #292629;
        font-family: 'Source Sans 3', sans-serif;
        font-size: 14px;
    }

    .category-count {
        color: #641F30;
        font-family: 'Cormorant Garamond', serif;
        font-size: 20px;
        font-weight: 600;
    }

    .category-heading {
        color: #641F30;
        font-family: 'Cormorant Garamond', serif;
        font-size: 23px;
        margin-bottom: 8px;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown(
        '<div class="overview-eyebrow">YOUR COLLECTION</div>',
        unsafe_allow_html=True
    )

    col1, col2 = st.columns([1, 2])

    with col1:
        st.markdown(
            f"""
            <div class="overview-total">{total}</div>
            <div class="overview-description">Garments in your collection</div>
            """,
            unsafe_allow_html=True
        )


    st.markdown(
        '<div class="overview-divider"></div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="category-heading">Collection by category</div>',
        unsafe_allow_html=True
    )

    category_columns = st.columns(4)

    for index, (category, label) in enumerate(category_order):
        with category_columns[index % 4]:
            count = category_counts.get(category, 0)

            st.markdown(
                f"""
                <div class="category-row">
                    <span class="category-name">{label}</span>
                    <span class="category-count">{count}</span>
                </div>
                """,
                unsafe_allow_html=True
            )


def render_wardrobe():

    st.title("My Wardrobe")

    st.markdown(
        "### A considered collection of everything you own."
    )

    db = SessionLocal()

    try:

        items = get_all_clothing(db)

        render_collection_overview(items)

        # ---------------------------------
        # ADD CLOTHING FORM
        # ---------------------------------

        with st.expander("＋ Add a garment", expanded=False):

            st.subheader("Garment details")

            add_category = st.selectbox(
                "Category",
                CATEGORY_OPTIONS,
                key="add_category",
            )

            with st.form("add_clothing_form"):

                name = st.text_input("Garment name")

                subcategory = st.selectbox(
                    "Subcategory",
                    SUBCATEGORY_OPTIONS[add_category],
                    key=f"add_subcategory_{add_category}",
                )

                st.divider()
                st.subheader("Appearance")

                col1, col2 = st.columns(2)

                with col1:
                    primary_colour = st.selectbox(
                        "Primary colour",
                        COLOUR_OPTIONS,
                    )

                with col2:
                    secondary_colour = st.text_input(
                        "Secondary colour (optional)"
                    )

                col1, col2 = st.columns(2)

                with col1:
                    material = st.text_input(
                        "Material",
                        placeholder="e.g. Cotton, wool, denim",
                    )

                with col2:
                    fit = st.selectbox("Fit", FIT_OPTIONS)

                st.divider()
                st.subheader("Season and weather")

                seasons = st.multiselect(
                    "Suitable seasons",
                    SEASON_OPTIONS,
                )

                col1, col2 = st.columns(2)

                with col1:
                    min_temperature = st.number_input(
                        "Minimum suitable temperature (°C)",
                        value=5.0,
                        step=1.0,
                    )

                with col2:
                    max_temperature = st.number_input(
                        "Maximum suitable temperature (°C)",
                        value=25.0,
                        step=1.0,
                    )

                weather_suitability = st.multiselect(
                    "Suitable weather",
                    WEATHER_OPTIONS,
                )

                st.divider()
                st.subheader("Styling")

                formality = st.selectbox(
                    "Formality",
                    FORMALITY_OPTIONS,
                )

                tags_input = st.text_input(
                    "Custom tags",
                    placeholder="e.g. vintage, layering, everyday",
                )

                notes = st.text_area(
                    "Additional notes",
                    placeholder="Anything else you want VESTA to know...",
                )

                st.divider()

                uploaded_image = st.file_uploader(
                    "Garment photograph",
                    type=["jpg", "jpeg", "png", "webp"],
                )

                submitted = st.form_submit_button(
                    "Add to My Wardrobe",
                    use_container_width=True,
                )

                if submitted:

                    if not name.strip():
                        st.error("Please enter a garment name.")

                    elif min_temperature > max_temperature:
                        st.error(
                            "Maximum temperature must be higher "
                            "than minimum temperature."
                        )

                    else:
                        try:
                            image_path = save_clothing_image(
                                uploaded_image
                            )

                            tags = [
                                tag.strip()
                                for tag in tags_input.split(",")
                                if tag.strip()
                            ]

                            add_clothing(
                                db=db,
                                name=name,
                                category=add_category,
                                subcategory=subcategory,
                                primary_colour=primary_colour,
                                secondary_colour=secondary_colour,
                                material=material,
                                fit=fit,
                                seasons=seasons,
                                min_temperature=min_temperature,
                                max_temperature=max_temperature,
                                weather_suitability=weather_suitability,
                                formality=formality,
                                notes=notes,
                                tags=tags,
                                image_path=image_path,
                            )

                            st.success(
                                f"{name} has been added to your wardrobe!"
                            )

                            st.rerun()

                        except (ValueError, OSError) as error:
                            st.error(str(error))

        # ---------------------------------
        # WARDROBE DISPLAY
        # ---------------------------------

        st.divider()


        if not items:

            st.info(
                "Your wardrobe is waiting to be filled. "
                "Add your first garment above."
            )

        else:

            # ---------------------------------
            # SEARCH AND FILTERS
            # ---------------------------------

            search = st.text_input(
                "Search your wardrobe",
                placeholder="Search by name, colour, material or tag...",
            )

            col1, col2 = st.columns(2)

            categories = sorted(
                set(item.category for item in items if item.category)
            )

            colours = sorted(
                set(item.primary_colour for item in items if item.primary_colour)
            )

            with col1:
                selected_category = st.selectbox(
                    "Filter by category",
                    ["All categories"] + categories,
                )

            with col2:
                selected_colour = st.selectbox(
                    "Filter by colour",
                    ["All colours"] + colours,
                )

            col1, col2 = st.columns(2)

            with col1:
                selected_seasons = st.multiselect(
                    "Filter by season",
                    SEASON_OPTIONS,
                    placeholder="All seasons",
                )

            formalities = sorted(
                set(item.formality for item in items if item.formality)
            )

            with col2:
                selected_formality = st.selectbox(
                    "Filter by formality",
                    ["All levels"] + formalities,
                )

            filtered_items = items

            if search:
                search_term = search.lower().strip()

                filtered_items = [
                    item for item in filtered_items
                    if search_term in (item.name or "").lower()
                    or search_term in (item.primary_colour or "").lower()
                    or search_term in (item.secondary_colour or "").lower()
                    or search_term in (item.category or "").lower()
                    or search_term in (item.subcategory or "").lower()
                    or search_term in (item.material or "").lower()
                    or any(
                        search_term in tag.name.lower()
                        for tag in item.tags
                    )
                ]

            if selected_category != "All categories":
                filtered_items = [
                    item for item in filtered_items
                    if item.category == selected_category
                ]

            if selected_colour != "All colours":
                filtered_items = [
                    item for item in filtered_items
                    if item.primary_colour == selected_colour
                ]

            if selected_seasons:
                filtered_items = [
                    item for item in filtered_items
                    if any(
                        season in [
                            s.strip()
                            for s in (item.seasons or "").split(",")
                        ]
                        for season in selected_seasons
                    )
                ]

            if selected_formality != "All levels":
                filtered_items = [
                    item for item in filtered_items
                    if item.formality == selected_formality
                ]

            # ---------------------------------
            # SORTING
            # ---------------------------------

            sort_option = st.selectbox(
                "Sort wardrobe by",
                [
                    "Recently added",
                    "Name (A–Z)",
                    "Category",
                    "Colour (A–Z)",
                ],
            )

            if sort_option == "Recently added":
                filtered_items = sorted(
                    filtered_items,
                    key=lambda item: item.created_at,
                    reverse=True,
                )

            elif sort_option == "Name (A–Z)":
                filtered_items = sorted(
                    filtered_items,
                    key=lambda item: item.name.lower(),
                )

            elif sort_option == "Category":
                filtered_items = sorted(
                    filtered_items,
                    key=lambda item: (item.category or "").lower(),
                )

            elif sort_option == "Colour (A–Z)":
                filtered_items = sorted(
                    filtered_items,
                    key=lambda item: (item.primary_colour or "").lower(),
                )

            st.caption(
                f"Showing {len(filtered_items)} of {len(items)} garments"
            )

            # ---------------------------------
            # GARMENT CARDS
            # ---------------------------------

            columns = st.columns(3)

            for index, item in enumerate(filtered_items):

                with columns[index % 3]:

                    if item.image_path:

                        image_file = (
                            Path(__file__).resolve().parent.parent
                            / item.image_path
                        )

                        if image_file.exists():
                            st.image(
                                str(image_file),
                                use_container_width=True,
                            )
                        else:
                            st.info("Image unavailable")

                    else:
                        st.markdown("◇ No photograph uploaded")

                    st.markdown(f"**{item.name}**")

                    st.caption(
                        f"{item.category} · {item.subcategory or 'Unspecified'} · "
                        f"{item.primary_colour}"
                    )

                    if item.material:
                        st.caption(item.material)

                    if item.tags:
                        st.caption(
                            " · ".join(tag.name for tag in item.tags)
                        )

                    # ---------------------------------
                    # GARMENT DETAILS
                    # ---------------------------------

                    with st.expander("Garment details"):

                        st.write(f"**Formality:** {item.formality}")

                        st.write(f"**Fit:** {item.fit or 'Not specified'}")

                        st.write(
                            f"**Temperature:** "
                            f"{item.min_temperature}°C – "
                            f"{item.max_temperature}°C"
                        )

                        st.write(
                            f"**Seasons:** {item.seasons or 'Not specified'}"
                        )

                        st.write(
                            f"**Weather:** "
                            f"{item.weather_suitability or 'Not specified'}"
                        )

                        if item.notes:
                            st.write(item.notes)

                    # ---------------------------------
                    # EDIT GARMENT
                    # ---------------------------------

                    with st.expander("Edit garment"):

                        edit_category = st.selectbox(
                            "Category",
                            CATEGORY_OPTIONS,
                            index=(
                                CATEGORY_OPTIONS.index(item.category)
                                if item.category in CATEGORY_OPTIONS
                                else 0
                            ),
                            key=f"edit_category_{item.id}",
                        )

                        edit_subcategory_options = get_subcategory_options(
                            edit_category,
                            item.subcategory if edit_category == item.category else None,
                        )

                        with st.form(f"edit_garment_{item.id}"):

                            st.subheader("Edit garment details")

                            edit_name = st.text_input(
                                "Garment name",
                                value=item.name,
                            )

                            edit_subcategory = st.selectbox(
                                "Subcategory",
                                edit_subcategory_options,
                                index=(
                                    edit_subcategory_options.index(item.subcategory)
                                    if item.subcategory in edit_subcategory_options
                                    else 0
                                ),
                                key=f"edit_subcategory_{item.id}_{edit_category}",
                            )

                            edit_colour = st.selectbox(
                                "Primary colour",
                                COLOUR_OPTIONS,
                                index=(
                                    COLOUR_OPTIONS.index(item.primary_colour)
                                    if item.primary_colour in COLOUR_OPTIONS
                                    else 0
                                ),
                            )

                            edit_secondary_colour = st.text_input(
                                "Secondary colour",
                                value=item.secondary_colour or "",
                            )

                            edit_material = st.text_input(
                                "Material",
                                value=item.material or "",
                            )

                            edit_fit = st.selectbox(
                                "Fit",
                                FIT_OPTIONS,
                                index=(
                                    FIT_OPTIONS.index(item.fit)
                                    if item.fit in FIT_OPTIONS
                                    else 0
                                ),
                            )

                            edit_seasons = st.multiselect(
                                "Suitable seasons",
                                SEASON_OPTIONS,
                                default=[
                                    s.strip()
                                    for s in (item.seasons or "").split(",")
                                    if s.strip() in SEASON_OPTIONS
                                ],
                            )

                            col1, col2 = st.columns(2)

                            with col1:
                                edit_min_temperature = st.number_input(
                                    "Minimum temperature (°C)",
                                    value=float(
                                        item.min_temperature
                                        if item.min_temperature is not None
                                        else 0
                                    ),
                                    step=1.0,
                                )

                            with col2:
                                edit_max_temperature = st.number_input(
                                    "Maximum temperature (°C)",
                                    value=float(
                                        item.max_temperature
                                        if item.max_temperature is not None
                                        else 25
                                    ),
                                    step=1.0,
                                )

                            edit_weather = st.multiselect(
                                "Suitable weather",
                                WEATHER_OPTIONS,
                                default=[
                                    w.strip()
                                    for w in (item.weather_suitability or "").split(",")
                                    if w.strip() in WEATHER_OPTIONS
                                ],
                            )

                            edit_formality = st.selectbox(
                                "Formality",
                                FORMALITY_OPTIONS,
                                index=(
                                    FORMALITY_OPTIONS.index(item.formality)
                                    if item.formality in FORMALITY_OPTIONS
                                    else 0
                                ),
                            )

                            edit_tags = st.text_input(
                                "Custom tags",
                                value=", ".join(tag.name for tag in item.tags),
                            )

                            edit_notes = st.text_area(
                                "Additional notes",
                                value=item.notes or "",
                            )

                            st.caption(
                                "Upload a new photograph only if you "
                                "want to replace the existing one."
                            )

                            replacement_image = st.file_uploader(
                                "Replace garment photograph",
                                type=["jpg", "jpeg", "png", "webp"],
                                key=f"edit_image_{item.id}",
                            )

                            save_changes = st.form_submit_button(
                                "Save changes",
                                use_container_width=True,
                            )

                            if save_changes:

                                if not edit_name.strip():
                                    st.error("Please enter a garment name.")

                                elif edit_min_temperature > edit_max_temperature:
                                    st.error(
                                        "Maximum temperature must be "
                                        "higher than minimum temperature."
                                    )

                                else:

                                    try:
                                        new_image_path = None

                                        if replacement_image is not None:
                                            new_image_path = save_clothing_image(
                                                replacement_image
                                            )

                                        updated_tags = [
                                            tag.strip()
                                            for tag in edit_tags.split(",")
                                            if tag.strip()
                                        ]

                                        update_clothing(
                                            db=db,
                                            item_id=item.id,
                                            name=edit_name,
                                            category=edit_category,
                                            subcategory=edit_subcategory,
                                            primary_colour=edit_colour,
                                            secondary_colour=edit_secondary_colour,
                                            material=edit_material,
                                            fit=edit_fit,
                                            seasons=edit_seasons,
                                            min_temperature=edit_min_temperature,
                                            max_temperature=edit_max_temperature,
                                            weather_suitability=edit_weather,
                                            formality=edit_formality,
                                            notes=edit_notes,
                                            tags=updated_tags,
                                            image_path=new_image_path,
                                        )

                                        st.success(
                                            f"{edit_name} has been updated!"
                                        )

                                        st.rerun()

                                    except (ValueError, OSError) as error:
                                        st.error(str(error))

                        if st.button(
                            "Delete garment",
                            key=f"delete_{item.id}",
                        ):
                            delete_clothing(db, item.id)
                            st.success("Garment deleted.")
                            st.rerun()

    finally:
        db.close()
