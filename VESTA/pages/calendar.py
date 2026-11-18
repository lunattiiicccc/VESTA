
import calendar as pycalendar
from datetime import date

import streamlit as st

from database.connection import SessionLocal
from services.clothing_service import get_all_clothing
from services.calendar_service import (
    add_calendar_event,
    get_calendar_events,
    get_events_for_date,
    delete_calendar_event,
)


# -----------------------------------------
# CALENDAR HELPERS
# -----------------------------------------

def change_month(current_month, direction):

    month = current_month.month + direction
    year = current_month.year

    if month < 1:
        month = 12
        year -= 1

    elif month > 12:
        month = 1
        year += 1

    return date(year, month, 1)


def get_month_dates(year, month):

    return pycalendar.monthcalendar(year, month)


# -----------------------------------------
# CALENDAR PAGE
# -----------------------------------------

def render_calendar():

    st.title("Outfit Calendar")

    st.write(
        "Plan your outfits ahead of time and organise "
        "what you'll wear."
    )

    today = date.today()

    # ---------------------------------
    # INITIALISE SESSION STATE
    # ---------------------------------

    if "vesta_calendar_month" not in st.session_state:
        st.session_state["vesta_calendar_month"] = date(
            today.year,
            today.month,
            1,
        )

    if "vesta_selected_date" not in st.session_state:
        st.session_state["vesta_selected_date"] = today

    current_month = st.session_state["vesta_calendar_month"]
    selected_date = st.session_state["vesta_selected_date"]

    db = SessionLocal()

    try:

        # ---------------------------------
        # LOAD WARDROBE
        # ---------------------------------

        wardrobe = get_all_clothing(db)

        # ---------------------------------
        # MONTH NAVIGATION
        # ---------------------------------

        st.subheader("Your calendar")

        nav_col1, nav_col2, nav_col3 = st.columns([1, 3, 1])

        with nav_col1:

            if st.button(
                "← Previous",
                use_container_width=True,
            ):

                st.session_state["vesta_calendar_month"] = (
                    change_month(current_month, -1)
                )

                st.rerun()

        with nav_col2:

            st.markdown(
                f"<h3 style='text-align:center;'>"
                f"{current_month.strftime('%B %Y')}"
                f"</h3>",
                unsafe_allow_html=True,
            )

        with nav_col3:

            if st.button(
                "Next →",
                use_container_width=True,
            ):

                st.session_state["vesta_calendar_month"] = (
                    change_month(current_month, 1)
                )

                st.rerun()

        if st.button("Today"):

            st.session_state["vesta_calendar_month"] = date(
                today.year,
                today.month,
                1,
            )

            st.session_state["vesta_selected_date"] = today

            st.rerun()

        # ---------------------------------
        # LOAD MONTH'S EVENTS
        # ---------------------------------

        last_day = pycalendar.monthrange(
            current_month.year,
            current_month.month,
        )[1]

        month_events = get_calendar_events(
            db,
            start_date=date(
                current_month.year,
                current_month.month,
                1,
            ),
            end_date=date(
                current_month.year,
                current_month.month,
                last_day,
            ),
        )

        event_counts = {}

        for event in month_events:

            event_counts[event.event_date] = (
                event_counts.get(event.event_date, 0) + 1
            )

        # ---------------------------------
        # MONTHLY CALENDAR GRID
        # ---------------------------------

        st.divider()

        weekday_names = [
            "Mon",
            "Tue",
            "Wed",
            "Thu",
            "Fri",
            "Sat",
            "Sun",
        ]

        weekday_columns = st.columns(7)

        for column, weekday in zip(
            weekday_columns,
            weekday_names,
        ):

            with column:

                st.markdown(
                    f"<div style='text-align:center;"
                    f"font-weight:bold;color:#873B4C;'>"
                    f"{weekday}</div>",
                    unsafe_allow_html=True,
                )

        weeks = get_month_dates(
            current_month.year,
            current_month.month,
        )

        for week_index, week in enumerate(weeks):

            day_columns = st.columns(7)

            for column_index, day_number in enumerate(week):

                with day_columns[column_index]:

                    if day_number == 0:

                        st.write("")

                    else:

                        calendar_date = date(
                            current_month.year,
                            current_month.month,
                            day_number,
                        )

                        count = event_counts.get(
                            calendar_date,
                            0,
                        )

                        label = str(day_number)

                        if count:
                            label += f"\n{count} planned"

                        if calendar_date == selected_date:
                            label = f"● {label}"

                        if st.button(
                            label,
                            key=f"calendar_{current_month.year}_{current_month.month}_{day_number}",
                            use_container_width=True,
                        ):

                            st.session_state[
                                "vesta_selected_date"
                            ] = calendar_date

                            st.rerun()

        # ---------------------------------
        # SELECTED DATE
        # ---------------------------------

        selected_date = st.session_state["vesta_selected_date"]

        st.divider()

        st.subheader(
            selected_date.strftime("%A, %d %B %Y")
        )

        selected_events = get_events_for_date(
            db,
            selected_date,
        )

        # ---------------------------------
        # DISPLAY PLANNED OUTFITS
        # ---------------------------------

        if selected_events:

            st.write("**Planned outfits**")

            for event in selected_events:

                with st.container(border=True):

                    st.markdown(
                        f"**{event.occasion or 'Planned outfit'}**"
                    )

                    if event.items:

                        for item in event.items:

                            st.write(
                                f"- {item.name} ({item.category})"
                            )

                    if event.notes:

                        st.caption(event.notes)

                    if st.button(
                        "Remove this plan",
                        key=f"delete_event_{event.id}",
                    ):

                        delete_calendar_event(
                            db,
                            event.id,
                        )

                        st.success("Outfit plan removed.")

                        st.rerun()

        else:

            st.info(
                "Nothing planned for this day yet."
            )

        # ---------------------------------
        # ADD NEW OUTFIT PLAN
        # ---------------------------------

        st.divider()

        st.subheader("Plan an outfit")

        if not wardrobe:

            st.warning(
                "Your wardrobe is empty. Add some garments "
                "before planning an outfit."
            )

        else:

            with st.form("add_calendar_event_form"):

                occasion = st.selectbox(
                    "Occasion",
                    [
                        "Everyday",
                        "University",
                        "Work",
                        "Smart Casual",
                        "Formal",
                        "Evening",
                        "Social",
                        "Special Occasion",
                        "Other",
                    ],
                )

                selected_items = st.multiselect(
                    "Choose garments",
                    options=wardrobe,
                    format_func=lambda item: (
                        f"{item.name} ({item.category})"
                    ),
                )

                notes = st.text_area(
                    "Notes (optional)",
                    placeholder=(
                        "Add any reminders or styling ideas..."
                    ),
                )

                submitted = st.form_submit_button(
                    "Save Outfit Plan",
                    type="primary",
                    use_container_width=True,
                )

                if submitted:

                    if not selected_items:

                        st.error(
                            "Please select at least one garment."
                        )

                    else:

                        try:

                            add_calendar_event(
                                db=db,
                                event_date=selected_date,
                                items=selected_items,
                                occasion=occasion,
                                notes=notes.strip() or None,
                            )

                            st.success(
                                "Your outfit has been added "
                                "to the calendar!"
                            )

                            st.rerun()

                        except Exception as error:

                            st.error(
                                f"Couldn't save your outfit: {error}"
                            )

    finally:

        db.close()


# Backwards-compatible page function name

def render_calendar_page():
    render_calendar()
