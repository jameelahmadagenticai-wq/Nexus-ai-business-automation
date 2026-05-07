import streamlit as st

from auth import login_page


# =========================
# PAGE CONFIG
# =========================

st.set_page_config(
    page_title="NexusOS AI",
    layout="wide"
)


# =========================
# SESSION INIT
# =========================

if "logged_in" not in st.session_state:

    st.session_state.logged_in = False

if "token" not in st.session_state:

    st.session_state.token = None


# =========================
# AUTH CHECK
# =========================

if not st.session_state.logged_in:

    login_page()

    st.stop()


# =========================
# PAGES
# =========================

dashboard_page = st.Page(

    "pages/dashboard.py",

    title="Dashboard",

    icon=":material/dashboard:",

    default=True
)


chat_page = st.Page(

    "pages/chat.py",

    title="Chat",

    icon=":material/chat:"
)


crm_page = st.Page(

    "pages/crm.py",

    title="CRM",

    icon=":material/groups:"
)


reports_page = st.Page(

    "pages/reports.py",

    title="Reports",

    icon=":material/description:"
)


email_dashboard_page = st.Page(

    "pages/email_dashboard.py",

    title="Email Dashboard",

    icon=":material/mail:"
)


settings_page = st.Page(

    "pages/settings.py",

    title="Settings",

    icon=":material/settings:"
)


# =========================
# NAVIGATION
# =========================

pg = st.navigation([

    dashboard_page,

    chat_page,

    crm_page,

    reports_page,

    email_dashboard_page,

    settings_page
])


# =========================
# RUN APP
# =========================

pg.run()