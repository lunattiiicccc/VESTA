
import streamlit as st

from database.connection import SessionLocal
from database.models import ClothingItem, CalendarEvent, SavedOutfit


# -----------------------------------------
# VESTA APPLICATION CONFIGURATION
# -----------------------------------------

st.set_page_config(
    page_title="VESTA | Your Digital Wardrobe",
    page_icon="♨️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.set_option("client.showSidebarNavigation", False)

PAGES = [
    "Dashboard",
    "My Wardrobe",
    "Outfit Studio",
    "Mockup Studio",
    "Outfit Calendar",
    "Saved Outfits"
]

PAGE_ICONS = {
    "Dashboard": ":material/dashboard:",
    "My Wardrobe": ":material/checkroom:",
    "Outfit Studio": ":material/auto_awesome:",
    "Mockup Studio": ":material/image:",
    "Outfit Calendar": ":material/calendar_month:",
    "Saved Outfits": ":material/bookmark_heart:"
}


# -----------------------------------------
# PAGE PERSISTENCE
# -----------------------------------------

if "page" not in st.session_state:
    requested_page = st.query_params.get("page", "Dashboard")

    if requested_page not in PAGES:
        requested_page = "Dashboard"

    st.session_state.page = requested_page


def select_page(page_name):
    st.session_state.page = page_name
    st.query_params["page"] = page_name


def go_to_wardrobe():
    select_page("My Wardrobe")


# -----------------------------------------
# DATABASE FUNCTIONS
# -----------------------------------------

def get_wardrobe_count():
    db = SessionLocal()

    try:
        return db.query(ClothingItem).count()
    finally:
        db.close()


def get_planned_outfit_count():
    db = SessionLocal()

    try:
        return db.query(CalendarEvent).count()
    finally:
        db.close()


def get_saved_outfit_count():
    db = SessionLocal()

    try:
        return db.query(SavedOutfit).count()
    finally:
        db.close()


# -----------------------------------------
# BRAND STYLING
# -----------------------------------------

st.markdown("""
<style>

/* -----------------------------------------
   FONTS
   ----------------------------------------- */

@import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;500;600;700&family=Cormorant+Garamond:wght@400;500;600;700&family=EB+Garamond:wght@400;500;600&family=Marcellus&family=Source+Sans+3:wght@400;500;600&family=Manrope:wght@400;500;600;700&display=swap');


/* -----------------------------------------
   VESTA COLOUR PALETTE
   ----------------------------------------- */

:root {
    --oxblood: #641F30;
    --burgundy: #873B4C;
    --parchment: #F1E9DC;
    --gold: #B39460;
    --charcoal: #292629;
    --rose: #C69B9D;
    --ivory: #F7F3EC;
    --white: #FFFFFF;
    --muted: #71666A;
    --border: #DCCFC1;
}


/* -----------------------------------------
   APPLICATION BACKGROUND
   ----------------------------------------- */

.stApp,
[data-testid="stAppViewContainer"],
[data-testid="stMain"] {
    background-color: var(--ivory) !important;
    color: var(--charcoal) !important;
}

.stApp {
    font-family: 'Source Sans 3', sans-serif;
}


/* -----------------------------------------
   TOP APPLICATION HEADER
   ----------------------------------------- */

header[data-testid="stHeader"] {
    background-color: var(--ivory) !important;
}

header[data-testid="stHeader"] button {
    color: var(--charcoal) !important;
}

header[data-testid="stHeader"] svg {
    color: var(--charcoal) !important;
    fill: var(--charcoal) !important;
}

[data-testid="stToolbar"] {
    background-color: var(--ivory) !important;
}


/* -----------------------------------------
   TYPOGRAPHY
   ----------------------------------------- */

h1, h2, h3, h4 {
    font-family: 'Cormorant Garamond', serif !important;
    color: var(--oxblood) !important;
}

p, li {
    color: var(--charcoal);
}

[data-testid="stCaptionContainer"],
[data-testid="stCaptionContainer"] p {
    color: var(--muted) !important;
}


/* -----------------------------------------
   SIDEBAR BACKGROUND
   ----------------------------------------- */

[data-testid="stSidebar"],
[data-testid="stSidebar"] > div,
[data-testid="stSidebarContent"] {
    background-color: var(--charcoal) !important;
}

[data-testid="stSidebar"] {
    border-right: 1px solid #50434A;
}

[data-testid="stSidebar"] p,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] span {
    color: var(--parchment);
}


/* -----------------------------------------
   VESTA BRANDING
   ----------------------------------------- */

.vesta-logo {
    font-family: 'Cinzel', serif;
    font-size: 40px;
    font-weight: 600;
    letter-spacing: 8px;
    color: var(--parchment);
    text-align: center;
    padding: 24px 0 4px 0;
}

.vesta-subtitle {
    font-family: 'Marcellus', serif;
    font-size: 10px;
    letter-spacing: 3px;
    color: var(--gold);
    text-align: center;
    padding-bottom: 20px;
}

.gold-line {
    border: none;
    border-top: 1px solid var(--gold);
    margin: 8px 0 27px 0;
}

.navigation-heading {
    font-family: 'Manrope', sans-serif;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 2px;
    color: var(--gold);
    padding: 0 0 12px 5px;
}

.sidebar-footer {
    font-family: 'EB Garamond', serif;
    font-size: 15px;
    font-style: italic;
    color: var(--rose);
    text-align: center;
    padding-top: 18px;
}


/* -----------------------------------------
   SIDEBAR NAVIGATION
   ----------------------------------------- */

[data-testid="stSidebar"] div[data-testid="stButton"] {
    margin: 0 0 6px 0;
}

[data-testid="stSidebar"] div[data-testid="stButton"] > button {
    width: 100%;
    min-height: 48px;
    padding: 0 16px;
    display: flex;
    align-items: center;
    justify-content: flex-start;
    gap: 13px;

    border-radius: 4px;
    font-family: 'Manrope', sans-serif;
    font-size: 13px;
    font-weight: 500;
    letter-spacing: 0.4px;

    box-shadow: none !important;
    transition: background-color 0.2s ease,
                border-color 0.2s ease;
}

/* Navigation icons */

[data-testid="stSidebar"] div[data-testid="stButton"] > button svg {
    width: 19px !important;
    height: 19px !important;
    min-width: 19px;
    color: var(--gold) !important;
    fill: none !important;
}

/* Inactive navigation items */

[data-testid="stSidebar"] div[data-testid="stButton"] > button[kind="secondary"] {
    background: transparent !important;
    color: var(--parchment) !important;
    border: 1px solid transparent !important;
}

[data-testid="stSidebar"] div[data-testid="stButton"] > button[kind="secondary"] span {
    color: var(--parchment) !important;
}

/* Hover effect */

[data-testid="stSidebar"] div[data-testid="stButton"] > button[kind="secondary"]:hover {
    background: #40353B !important;
    border-color: #65515A !important;
}

[data-testid="stSidebar"] div[data-testid="stButton"] > button[kind="secondary"]:hover svg {
    color: var(--rose) !important;
}

/* Active navigation item */

[data-testid="stSidebar"] div[data-testid="stButton"] > button[kind="primary"] {
    background: var(--oxblood) !important;
    color: var(--parchment) !important;
    border: 1px solid var(--gold) !important;
    border-left: 4px solid var(--gold) !important;
}

[data-testid="stSidebar"] div[data-testid="stButton"] > button[kind="primary"] span {
    color: var(--parchment) !important;
}

[data-testid="stSidebar"] div[data-testid="stButton"] > button[kind="primary"] svg {
    color: var(--gold) !important;
}


/* -----------------------------------------
   DASHBOARD
   ----------------------------------------- */

.welcome-title {
    font-family: 'Cormorant Garamond', serif;
    font-size: 44px;
    color: var(--oxblood);
    margin-bottom: 0;
}

.welcome-subtitle {
    font-family: 'EB Garamond', serif;
    font-size: 19px;
    color: var(--muted);
}


/* -----------------------------------------
   METRIC CARDS
   ----------------------------------------- */

.metric-card {
    background: var(--white);
    border: 1px solid var(--border);
    border-top: 3px solid var(--gold);
    padding: 22px;
    border-radius: 4px;
    min-height: 115px;
}

.metric-label {
    font-family: 'Manrope', sans-serif;
    font-size: 11px;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    color: var(--muted);
}

.metric-value {
    font-family: 'Cormorant Garamond', serif;
    font-size: 35px;
    color: var(--oxblood);
}


/* -----------------------------------------
   MAIN BUTTONS
   ----------------------------------------- */

.stApp div[data-testid="stButton"] > button {
    background-color: var(--oxblood) !important;
    color: var(--white) !important;
    border: 1px solid var(--oxblood) !important;
    border-radius: 4px;
    font-family: 'Manrope', sans-serif;
    font-size: 13px;
}

.stApp div[data-testid="stButton"] > button * {
    color: var(--white) !important;
    -webkit-text-fill-color: var(--white) !important;
    fill: var(--white) !important;
}

.stApp div[data-testid="stButton"] > button:hover {
    background-color: var(--burgundy) !important;
    border-color: var(--gold) !important;
}

/* Sidebar button overrides */

[data-testid="stSidebar"] div[data-testid="stButton"] > button[kind="secondary"] {
    background-color: transparent !important;
    color: var(--parchment) !important;
    border-color: transparent !important;
}

[data-testid="stSidebar"] div[data-testid="stButton"] > button[kind="primary"] {
    background-color: var(--oxblood) !important;
    color: var(--parchment) !important;
    border-color: var(--gold) !important;
    border-left: 4px solid var(--gold) !important;
}

[data-testid="stSidebar"] div[data-testid="stButton"] > button span,
[data-testid="stSidebar"] div[data-testid="stButton"] > button svg {
    color: var(--parchment) !important;
    fill: var(--parchment) !important;
}


/* -----------------------------------------
   INPUTS
   ----------------------------------------- */

.stApp input,
.stApp textarea,
.stApp [data-baseweb="input"] {
    background-color: var(--white) !important;
    color: var(--charcoal) !important;
    -webkit-text-fill-color: var(--charcoal) !important;
    border-color: #CDBEAE !important;
}

.stApp input::placeholder,
.stApp textarea::placeholder {
    color: var(--muted) !important;
    -webkit-text-fill-color: var(--muted) !important;
    opacity: 1;
}


/* -----------------------------------------
   DROPDOWNS AND MULTISELECT
   ----------------------------------------- */

.stApp [data-baseweb="select"] > div {
    background-color: var(--white) !important;
    color: var(--charcoal) !important;
    border-color: #CDBEAE !important;
}

.stApp [data-baseweb="select"] span {
    color: var(--charcoal) !important;
}

.stApp [data-baseweb="select"] input {
    color: var(--charcoal) !important;
    -webkit-text-fill-color: var(--charcoal) !important;
}

.stApp [data-baseweb="tag"] {
    background-color: var(--parchment) !important;
    border: 1px solid var(--border) !important;
}

.stApp [data-baseweb="tag"] span {
    color: var(--oxblood) !important;
}

[data-baseweb="popover"],
[data-baseweb="menu"],
[role="listbox"] {
    background-color: var(--white) !important;
}

[role="option"] {
    background-color: var(--white) !important;
    color: var(--charcoal) !important;
}

[role="option"]:hover,
[aria-selected="true"] {
    background-color: var(--parchment) !important;
    color: var(--oxblood) !important;
}


/* -----------------------------------------
   FORM LABELS
   ----------------------------------------- */

[data-testid="stWidgetLabel"] p,
.stApp label {
    color: var(--charcoal) !important;
}

.stApp [data-testid="stCheckbox"] p,
.stApp [data-testid="stRadio"] p {
    color: var(--charcoal) !important;
}


/* -----------------------------------------
   FILE UPLOADER
   ----------------------------------------- */

.stApp [data-testid="stFileUploader"] {
    background: var(--parchment) !important;
    background-color: var(--parchment) !important;
    border: 1px solid var(--border) !important;
    border-radius: 5px !important;
    padding: 10px !important;
}

.stApp [data-testid="stFileUploaderDropzone"] {
    background: var(--parchment) !important;
    background-color: var(--parchment) !important;
    border: 1px dashed #B39460 !important;
    border-radius: 5px !important;
}

.stApp [data-testid="stFileUploader"] p,
.stApp [data-testid="stFileUploader"] span,
.stApp [data-testid="stFileUploader"] small,
.stApp [data-testid="stFileUploader"] label {
    color: var(--charcoal) !important;
    -webkit-text-fill-color: var(--charcoal) !important;
}

.stApp [data-testid="stFileUploader"] button,
.stApp [data-testid="stFileUploaderDropzone"] button {
    background: var(--oxblood) !important;
    background-color: var(--oxblood) !important;
    border: 1px solid var(--oxblood) !important;
    color: #FFFFFF !important;
}

.stApp [data-testid="stFileUploader"] button *,
.stApp [data-testid="stFileUploaderDropzone"] button * {
    color: #FFFFFF !important;
    -webkit-text-fill-color: #FFFFFF !important;
    fill: #FFFFFF !important;
}

.stApp [data-testid="stFileUploader"] button:hover,
.stApp [data-testid="stFileUploaderDropzone"] button:hover {
    background: var(--burgundy) !important;
    background-color: var(--burgundy) !important;
    border-color: var(--gold) !important;
}


/* -----------------------------------------
   FORM SUBMISSION BUTTONS
   ----------------------------------------- */

.stApp [data-testid="stFormSubmitButton"] button,
.stApp [data-testid="stForm"] button {
    background: var(--oxblood) !important;
    background-color: var(--oxblood) !important;
    border: 1px solid var(--oxblood) !important;
    color: #FFFFFF !important;
}

.stApp [data-testid="stFormSubmitButton"] button *,
.stApp [data-testid="stForm"] button * {
    color: #FFFFFF !important;
    -webkit-text-fill-color: #FFFFFF !important;
    fill: #FFFFFF !important;
}

.stApp [data-testid="stFormSubmitButton"] button:hover,
.stApp [data-testid="stForm"] button:hover {
    background: var(--burgundy) !important;
    background-color: var(--burgundy) !important;
    border-color: var(--gold) !important;
}


/* -----------------------------------------
   ALERTS AND NOTIFICATIONS
   ----------------------------------------- */

.stApp [data-testid="stAlert"],
.stApp [data-baseweb="notification"] {
    background-color: var(--parchment) !important;
    border: 1px solid var(--border) !important;
    border-left: 4px solid var(--gold) !important;
    border-radius: 4px !important;
    color: var(--charcoal) !important;
}

.stApp [data-testid="stAlert"] > div,
.stApp [data-testid="stAlert"] [data-testid="stMarkdownContainer"],
.stApp [data-baseweb="notification"] > div {
    background-color: transparent !important;
}

.stApp [data-testid="stAlert"] *,
.stApp [data-baseweb="notification"] * {
    color: var(--charcoal) !important;
}

.stApp [data-testid="stAlert"] svg,
.stApp [data-baseweb="notification"] svg {
    color: var(--oxblood) !important;
    fill: var(--oxblood) !important;
}


/* -----------------------------------------
   EXPANDERS
   ----------------------------------------- */

.stApp [data-testid="stExpander"] {
    background-color: var(--white) !important;
    border: 1px solid var(--border) !important;
    border-radius: 4px !important;
}

.stApp [data-testid="stExpander"] summary {
    background-color: var(--white) !important;
}

.stApp [data-testid="stExpander"] summary,
.stApp [data-testid="stExpander"] summary span,
.stApp [data-testid="stExpander"] summary p {
    color: var(--oxblood) !important;
}

.stApp [data-testid="stExpander"] [data-testid="stMarkdownContainer"] p {
    color: var(--charcoal) !important;
}


/* -----------------------------------------
   BORDERED CONTAINERS
   ----------------------------------------- */

.stApp [data-testid="stVerticalBlockBorderWrapper"] {
    background-color: var(--white) !important;
    border: 1px solid var(--border) !important;
    border-radius: 4px !important;
}


/* -----------------------------------------
   METRICS
   ----------------------------------------- */

.stApp [data-testid="stMetricLabel"],
.stApp [data-testid="stMetricLabel"] p {
    color: var(--muted) !important;
}

.stApp [data-testid="stMetricValue"],
.stApp [data-testid="stMetricValue"] div {
    color: var(--oxblood) !important;
}


/* -----------------------------------------
   DIVIDERS
   ----------------------------------------- */

hr {
    border-color: var(--border);
}

</style>
""", unsafe_allow_html=True)


# -----------------------------------------
# SIDEBAR NAVIGATION
# -----------------------------------------

with st.sidebar:

    st.markdown(
        '<div class="vesta-logo">VESTA</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="vesta-subtitle">'
        'VESTI, VIDI, VICI.'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<hr class="gold-line">',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="navigation-heading">YOUR SPACE</div>',
        unsafe_allow_html=True
    )

    for navigation_page in PAGES:

        is_selected = st.session_state.page == navigation_page

        st.button(
            navigation_page,
            key=f"navigation_{navigation_page}",
            icon=PAGE_ICONS[navigation_page],
            type="primary" if is_selected else "secondary",
            use_container_width=True,
            on_click=select_page,
            args=(navigation_page,)
        )

    st.markdown("---")

    st.markdown(
        '<div class="sidebar-footer">'
        'Dress for the Day You Desire.'
        '</div>',
        unsafe_allow_html=True
    )


page = st.session_state.page


# -----------------------------------------
# DASHBOARD
# -----------------------------------------

if page == "Dashboard":

    wardrobe_count = get_wardrobe_count()
    planned_outfit_count = get_planned_outfit_count()
    saved_outfit_count = get_saved_outfit_count()

    st.markdown(
        '<div class="welcome-title">Welcome to VESTA</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="welcome-subtitle">'
        'Your wardrobe, thoughtfully reimagined.'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown("---")

    st.subheader("Your Wardrobe at a Glance")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">WARDROBE ITEMS</div>
            <div class="metric-value">{wardrobe_count}</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">SAVED OUTFITS</div>
            <div class="metric-value">{saved_outfit_count}</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">PLANNED OUTFITS</div>
            <div class="metric-value">{planned_outfit_count}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    st.subheader("Begin with your wardrobe")

    st.write(
        "Add your clothing, explore new combinations and "
        "discover more possibilities in the pieces you already own."
    )

    st.button(
        "Explore My Wardrobe",
        icon=":material/arrow_forward:",
        on_click=go_to_wardrobe
    )


# -----------------------------------------
# MY WARDROBE
# -----------------------------------------

elif page == "My Wardrobe":

    from pages.wardrobe import render_wardrobe
    render_wardrobe()


# -----------------------------------------
# OUTFIT STUDIO
# -----------------------------------------

elif page == "Outfit Studio":

    from pages.outfit_generator import render_outfit_generator
    render_outfit_generator()


# -----------------------------------------
# MOCKUP STUDIO
# -----------------------------------------

elif page == "Mockup Studio":

    from pages.mockup_studio import render_mockup_studio
    render_mockup_studio()


# -----------------------------------------
# OUTFIT CALENDAR
# -----------------------------------------

elif page == "Outfit Calendar":

    from pages.calendar import render_calendar
    render_calendar()


# -----------------------------------------
# SAVED OUTFITS
# -----------------------------------------

elif page == "Saved Outfits":

    from pages.saved_outfits import render_saved_outfits
    render_saved_outfits()
