
import streamlit as st
from io import BytesIO

from database.connection import SessionLocal
from services.clothing_service import get_all_clothing
from services.image_composer import compose_flat_lay


# -----------------------------------------
# PAGE
# -----------------------------------------

def render_mockup_studio():

    st.title("Mockup Studio")

    st.write(
        "Bring your wardrobe together and create a visual "
        "flat-lay of your outfit."
    )

    st.divider()

    db = SessionLocal()

    try:

        # ---------------------------------
        # LOAD WARDROBE
        # ---------------------------------

        wardrobe = get_all_clothing(db)

        if not wardrobe:

            st.warning(
                "Your wardrobe is empty. Add clothing items "
                "and upload their photographs before creating "
                "a mockup."
            )
            return

        photographed_items = [
            item for item in wardrobe
            if item.image_path
        ]

        if not photographed_items:

            st.warning(
                "You haven't uploaded any garment photographs yet. "
                "Visit My Wardrobe and add photographs to your items."
            )
            return

        # ---------------------------------
        # GARMENT SELECTION
        # ---------------------------------

        st.subheader("Build your outfit")

        st.write(
            "Choose the garments you'd like to include "
            "in your flat-lay."
        )

        categories = [
            "Top",
            "Bottom",
            "Dress",
            "Jumpsuit",
            "Outerwear",
            "Footwear",
            "Accessory",
        ]

        selected_items = []

        for category in categories:

            category_items = [
                item for item in photographed_items
                if item.category == category
            ]

            if not category_items:
                continue

            with st.expander(
                f"{category} ({len(category_items)} available)",
                expanded=category in [
                    "Top",
                    "Bottom",
                    "Dress",
                    "Footwear",
                ],
            ):

                selected_names = st.multiselect(
                    f"Choose {category.lower()} items",
                    options=category_items,
                    format_func=lambda item: item.name,
                    key=f"mockup_{category}",
                )

                selected_items.extend(selected_names)

        st.divider()

        # ---------------------------------
        # SELECTION SUMMARY
        # ---------------------------------

        st.subheader("Your selected garments")

        if selected_items:

            for item in selected_items:

                st.write(
                    f"- **{item.name}** ({item.category})"
                )

            st.caption(
                f"{len(selected_items)} garment(s) selected."
            )

        else:

            st.info(
                "Select some garments above to begin building "
                "your mockup."
            )

        st.divider()

        # ---------------------------------
        # GENERATE MOCKUP
        # ---------------------------------

        if st.button(
            "Create Flat-Lay Mockup",
            type="primary",
            use_container_width=True,
            disabled=not selected_items,
        ):

            try:

                mockup, missing_items = compose_flat_lay(
                    selected_items
                )

                st.session_state["vesta_mockup"] = mockup
                st.session_state["vesta_mockup_missing"] = missing_items

            except Exception as error:

                st.error(
                    f"VESTA couldn't create the mockup: {error}"
                )

        # ---------------------------------
        # DISPLAY MOCKUP
        # ---------------------------------

        if "vesta_mockup" in st.session_state:

            st.divider()

            st.subheader("Your outfit mockup")

            mockup = st.session_state["vesta_mockup"]

            st.image(
                mockup,
                use_container_width=True,
            )

            missing_items = st.session_state.get(
                "vesta_mockup_missing",
                [],
            )

            if missing_items:

                st.warning(
                    "These garments were skipped because their "
                    "photographs couldn't be loaded: "
                    + ", ".join(missing_items)
                )

            # ---------------------------------
            # PREPARE PNG DOWNLOAD
            # ---------------------------------

            image_buffer = BytesIO()

            mockup.save(
                image_buffer,
                format="PNG",
            )

            image_buffer.seek(0)

            # ---------------------------------
            # DOWNLOAD
            # ---------------------------------

            st.download_button(
                label="Download Mockup",
                data=image_buffer.getvalue(),
                file_name="vesta_outfit_mockup.png",
                mime="image/png",
                use_container_width=True,
            )

    finally:

        db.close()
