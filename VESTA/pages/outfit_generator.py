
import streamlit as st
from datetime import datetime, date
from io import BytesIO

from database.connection import SessionLocal
from services.clothing_service import get_all_clothing
from services.weather import get_current_weather
from services.calendar_service import add_calendar_event
from services.image_composer import (
    load_garment_image,
    compose_flat_lay,
)
from engine.generator import generate_outfits


# -----------------------------------------
# WEATHER RETRIEVAL
# -----------------------------------------

@st.cache_data(ttl=900)
def load_weather():
    """Retrieve and cache current weather for 15 minutes."""

    return get_current_weather("Huddersfield")


# -----------------------------------------
# SEASON DETECTION
# -----------------------------------------

def get_current_season():
    """Determine the current UK season from the date."""

    month = datetime.now().month

    if month in [3, 4, 5]:
        return "Spring"

    elif month in [6, 7, 8]:
        return "Summer"

    elif month in [9, 10, 11]:
        return "Autumn"

    else:
        return "Winter"


# -----------------------------------------
# OUTFIT GENERATOR PAGE
# -----------------------------------------

def render_outfit_generator():

    st.title("Outfit Generator")

    st.write(
        "Discover outfits created from your own wardrobe."
    )

    db = SessionLocal()

    try:

        # ---------------------------------
        # LOAD WARDROBE
        # ---------------------------------

        wardrobe = get_all_clothing(db)

        if not wardrobe:
            st.warning(
                "Your wardrobe is empty. "
                "Add some clothing items first."
            )
            return

        wardrobe_lookup = {
            item.id: item
            for item in wardrobe
        }

        # ---------------------------------
        # LOAD CURRENT WEATHER
        # ---------------------------------

        st.subheader("Current weather")

        weather_data = None

        try:

            weather_data = load_weather()

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric(
                    "Temperature",
                    f"{weather_data['temperature']}°C",
                )

            with col2:
                st.metric(
                    "Conditions",
                    weather_data["weather"],
                )

            with col3:
                st.metric(
                    "Wind speed",
                    f"{weather_data['wind_speed']} km/h"
                    if weather_data["wind_speed"] is not None
                    else "Unavailable",
                )

            st.caption(
                f"{weather_data['description']} · "
                f"{weather_data['location']} · "
                f"Updated: {weather_data['time']}"
            )

        except Exception:

            st.warning(
                "VESTA couldn't retrieve the current weather. "
                "You can still generate outfits using manual settings."
            )

        # ---------------------------------
        # OUTFIT PREFERENCES
        # ---------------------------------

        st.divider()

        st.subheader("What are you dressing for?")

        col1, col2 = st.columns(2)

        with col1:

            default_temperature = (
                int(round(weather_data["temperature"]))
                if weather_data
                else 15
            )

            temperature = st.slider(
                "Temperature (°C)",
                min_value=-10,
                max_value=35,
                value=max(
                    -10,
                    min(35, default_temperature)
                ),
                key="outfit_temperature_v2",
            )

            weather_options = [
                "Any",
                "Sunny",
                "Cloudy",
                "Rainy",
                "Snowy",
                "Windy",
            ]

            default_weather = (
                weather_data["weather"]
                if weather_data
                else "Any"
            )

            weather = st.selectbox(
                "Weather",
                weather_options,
                index=(
                    weather_options.index(default_weather)
                    if default_weather in weather_options
                    else 0
                ),
                key="outfit_weather_v2",
            )

        with col2:

            season_options = [
                "Any",
                "Spring",
                "Summer",
                "Autumn",
                "Winter",
            ]

            default_season = get_current_season()

            season = st.selectbox(
                "Season",
                season_options,
                index=season_options.index(default_season),
                key="outfit_season_v2",
            )

            formality = st.selectbox(
                "Occasion",
                [
                    "Any",
                    "Casual",
                    "Smart Casual",
                    "Business Casual",
                    "Formal",
                    "Evening",
                ],
                key="outfit_formality_v2",
            )

        st.caption(
            "Weather and season are automatically populated "
            "using current conditions and the calendar. "
            "You can change any setting manually."
        )

        st.divider()

        # ---------------------------------
        # GENERATE OUTFITS
        # ---------------------------------

        if st.button(
            "Generate Outfits",
            type="primary",
            use_container_width=True,
        ):

            outfits = generate_outfits(
                wardrobe,
                temperature=temperature,
                weather=(
                    None if weather == "Any" else weather
                ),
                season=(
                    None if season == "Any" else season
                ),
                formality=(
                    None if formality == "Any" else formality
                ),
                limit=3,
            )

            # Clear previous mockups when generating
            # a new set of recommendations.

            for key in list(st.session_state.keys()):

                if key.startswith("vesta_outfit_mockup_"):
                    del st.session_state[key]

            if not outfits:

                st.session_state["vesta_recommendations"] = []

                st.warning(
                    "We couldn't find any complete outfits "
                    "for those conditions. Try changing your "
                    "selections or adding more clothing."
                )

            else:

                saved_recommendations = []

                for outfit in outfits:

                    saved_recommendations.append({
                        "score": outfit["score"],
                        "breakdown": outfit["breakdown"],
                        "explanation": outfit["explanation"],
                        "item_ids": [
                            item.id
                            for item in outfit["items"]
                        ],
                    })

                st.session_state[
                    "vesta_recommendations"
                ] = saved_recommendations

        # ---------------------------------
        # DISPLAY RECOMMENDATIONS
        # ---------------------------------

        recommendations = st.session_state.get(
            "vesta_recommendations",
            [],
        )

        if recommendations:

            st.divider()

            st.subheader("Your outfit recommendations")

            st.write(
                "Choose a date and save any recommendation "
                "directly to your Outfit Calendar."
            )

            planned_date = st.date_input(
                "When would you like to wear these outfits?",
                value=date.today(),
                key="vesta_outfit_plan_date",
            )

            occasion = (
                formality
                if formality != "Any"
                else "Everyday"
            )

            st.divider()

            for index, recommendation in enumerate(
                recommendations,
                start=1,
            ):

                st.subheader(f"Outfit {index}")

                st.metric(
                    "Style match score",
                    f"{recommendation['score']:.1f}/100",
                )

                # Retrieve garments in the current session.

                outfit_items = [
                    wardrobe_lookup[item_id]
                    for item_id in recommendation["item_ids"]
                    if item_id in wardrobe_lookup
                ]

                st.write("### Your outfit")

                for item in outfit_items:

                    col1, col2 = st.columns([1, 4])

                    with col1:

                        if item.image_path:

                            garment_image = load_garment_image(item)

                            if garment_image:
                                st.image(
                                    garment_image,
                                    use_container_width=True,
                                )

                    with col2:

                        st.write(
                            f"**{item.category}:** {item.name}"
                        )

                        if item.primary_colour:
                            st.caption(item.primary_colour)

                st.write("**Why this outfit works**")

                for explanation in recommendation["explanation"]:

                    st.write(f"- {explanation}")

                with st.expander("View score breakdown"):

                    for category, score in recommendation[
                        "breakdown"
                    ].items():

                        st.write(
                            f"**{category.title()}:** {score}/100"
                        )

                # ---------------------------------
                # GENERATE OUTFIT MOCKUP
                # ---------------------------------

                st.divider()

                st.write("### Outfit visualisation")

                mockup_key = (
                    f"vesta_outfit_mockup_{index}"
                )

                if st.button(
                    "Generate Outfit Mockup",
                    key=f"generate_mockup_{index}",
                    use_container_width=True,
                ):

                    if not outfit_items:

                        st.error(
                            "The garments for this outfit "
                            "could not be found."
                        )

                    else:

                        try:

                            with st.spinner(
                                "Creating your outfit mockup..."
                            ):

                                mockup_image, missing_images = (
                                    compose_flat_lay(outfit_items)
                                )

                                image_buffer = BytesIO()

                                mockup_image.save(
                                    image_buffer,
                                    format="PNG",
                                )

                                st.session_state[mockup_key] = {
                                    "image": image_buffer.getvalue(),
                                    "missing": missing_images,
                                }

                        except Exception as error:

                            st.error(
                                f"Couldn't create the mockup: {error}"
                            )

                # Display previously generated mockup.

                if mockup_key in st.session_state:

                    mockup_data = st.session_state[mockup_key]

                    st.image(
                        mockup_data["image"],
                        use_container_width=True,
                    )

                    if mockup_data["missing"]:

                        st.warning(
                            "Some garments don't have usable "
                            "photographs, so placeholders may "
                            "appear in the mockup."
                        )

                    st.download_button(
                        label="Download Outfit Mockup",
                        data=mockup_data["image"],
                        file_name=f"vesta_outfit_{index}_mockup.png",
                        mime="image/png",
                        key=f"download_mockup_{index}",
                        use_container_width=True,
                    )

                # ---------------------------------
                # SAVE TO CALENDAR
                # ---------------------------------

                st.divider()

                if st.button(
                    "Save Outfit to Calendar",
                    key=f"save_outfit_{index}",
                    use_container_width=True,
                ):

                    if not outfit_items:

                        st.error(
                            "The garments for this recommendation "
                            "could not be found in your wardrobe."
                        )

                    else:

                        try:

                            add_calendar_event(
                                db=db,
                                event_date=planned_date,
                                items=outfit_items,
                                occasion=occasion,
                                notes=(
                                    f"Saved from Outfit Generator. "
                                    f"Style match score: "
                                    f"{recommendation['score']:.1f}/100."
                                ),
                            )

                            st.success(
                                f"Outfit {index} saved to your calendar "
                                f"for {planned_date.strftime('%d %B %Y')}!"
                            )

                        except Exception as error:

                            st.error(
                                f"Couldn't save this outfit: {error}"
                            )

                st.divider()

    finally:

        db.close()
