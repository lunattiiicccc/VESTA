
import streamlit as st

from database.connection import SessionLocal

from services.clothing_service import get_all_clothing

from services.saved_outfit_service import (
    add_saved_outfit,
    get_all_saved_outfits,
    update_saved_outfit,
    delete_saved_outfit,
)

from services.image_composer import load_garment_image


# -----------------------------------------
# PAGE STYLING
# -----------------------------------------

def render_saved_outfits():

    st.title("Saved Outfits")

    st.markdown(
        "A collection of looks worth keeping."
    )

    st.divider()

    db = SessionLocal()

    try:

        outfits = get_all_saved_outfits(db)
        clothing_items = get_all_clothing(db)

        # ---------------------------------
        # COLLECTION SUMMARY
        # ---------------------------------

        total_outfits = len(outfits)

        total_columns = st.columns(2)

        total_columns[0].metric(
            "Saved Outfits",
            total_outfits
        )

        total_columns[1].metric(
            "Wardrobe Garments",
            len(clothing_items)
        )

        st.divider()

        # ---------------------------------
        # ADD NEW OUTFIT
        # ---------------------------------

        with st.expander("＋ Create a Saved Outfit", expanded=False):

            if not clothing_items:

                st.info(
                    "Add garments to your wardrobe before creating an outfit."
                )

            else:

                with st.form("create_saved_outfit_form"):

                    outfit_name = st.text_input(
                        "Outfit name",
                        placeholder="e.g. Everyday University Outfit"
                    )

                    outfit_description = st.text_area(
                        "Description",
                        placeholder="Describe the outfit or when you like to wear it."
                    )

                    selected_items = st.multiselect(
                        "Choose garments",
                        options=clothing_items,
                        format_func=lambda item: (
                            f"{item.name} ({item.category})"
                        )
                    )

                    submitted = st.form_submit_button(
                        "Save Outfit",
                        use_container_width=True
                    )

                    if submitted:

                        if not outfit_name.strip():

                            st.error("Please give your outfit a name.")

                        elif not selected_items:

                            st.error("Please select at least one garment.")

                        else:

                            try:

                                add_saved_outfit(
                                    db=db,
                                    name=outfit_name,
                                    items=selected_items,
                                    description=outfit_description
                                )

                                st.success("Outfit saved successfully!")
                                st.rerun()

                            except Exception as error:

                                st.error(
                                    f"Unable to save outfit: {error}"
                                )

        st.divider()

        # ---------------------------------
        # DISPLAY SAVED OUTFITS
        # ---------------------------------

        st.subheader("Your Outfit Collection")

        if not outfits:

            st.info(
                "You haven't saved any outfits yet. "
                "Create your first outfit above."
            )

        else:

            for outfit in outfits:

                with st.container(border=True):

                    heading_col, date_col = st.columns([3, 1])

                    with heading_col:

                        st.subheader(outfit.name)

                    with date_col:

                        if outfit.created_at:

                            st.caption(
                                outfit.created_at.strftime("%d %b %Y")
                            )

                    if outfit.description:

                        st.write(outfit.description)

                    st.caption(
                        f"{len(outfit.items)} garments"
                    )

                    # GARMENT PHOTOGRAPHS

                    image_columns = st.columns(
                        min(len(outfit.items), 4)
                    )

                    for index, garment in enumerate(outfit.items):

                        with image_columns[index % len(image_columns)]:

                            garment_image = load_garment_image(garment)

                            if garment_image is not None:

                                st.image(
                                    garment_image,
                                    use_container_width=True
                                )

                            else:

                                st.markdown(
                                    "No photograph"
                                )

                            st.caption(garment.name)

                    # EDIT OUTFIT

                    with st.expander("Edit Outfit"):

                        with st.form(
                            f"edit_outfit_form_{outfit.id}"
                        ):

                            edited_name = st.text_input(
                                "Outfit name",
                                value=outfit.name,
                                key=f"edit_name_{outfit.id}"
                            )

                            edited_description = st.text_area(
                                "Description",
                                value=outfit.description or "",
                                key=f"edit_description_{outfit.id}"
                            )

                            edited_items = st.multiselect(
                                "Garments",
                                options=clothing_items,
                                default=[
                                    item for item in outfit.items
                                    if item.id in {
                                        garment.id
                                        for garment in clothing_items
                                    }
                                ],
                                format_func=lambda item: (
                                    f"{item.name} ({item.category})"
                                ),
                                key=f"edit_items_{outfit.id}"
                            )

                            update_submitted = st.form_submit_button(
                                "Update Outfit",
                                use_container_width=True
                            )

                            if update_submitted:

                                if not edited_name.strip():

                                    st.error(
                                        "Please give your outfit a name."
                                    )

                                elif not edited_items:

                                    st.error(
                                        "Please select at least one garment."
                                    )

                                else:

                                    try:

                                        update_saved_outfit(
                                            db=db,
                                            outfit_id=outfit.id,
                                            name=edited_name,
                                            items=edited_items,
                                            description=edited_description
                                        )

                                        st.success("Outfit updated!")
                                        st.rerun()

                                    except Exception as error:

                                        st.error(
                                            f"Unable to update outfit: {error}"
                                        )

                    # DELETE OUTFIT

                    if st.button(
                        "Delete Outfit",
                        key=f"delete_outfit_{outfit.id}"
                    ):

                        try:

                            delete_saved_outfit(db, outfit.id)

                            st.success("Outfit deleted.")
                            st.rerun()

                        except Exception as error:

                            st.error(
                                f"Unable to delete outfit: {error}"
                            )

    finally:

        db.close()
