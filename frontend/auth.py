import streamlit as st

from api_client import (
    login_user,
    register_user
)

# =========================
# AUTH PAGE
# =========================

def login_page():

    st.title("NexusOS Login")

    tab1, tab2 = st.tabs([
        "Login",
        "Register"
    ])

    # =========================
    # LOGIN TAB
    # =========================

    with tab1:

        username = st.text_input(
            "Username",
            key="login_username"
        )

        password = st.text_input(
            "Password",
            type="password",
            key="login_password"
        )

        if st.button("Login"):

            response = login_user(
                username=username,
                password=password
            )

            if response.get("access_token"):

                st.session_state.token = response["access_token"]

                st.session_state.logged_in = True

                st.success("Login successful")

                st.rerun()

            else:

                st.error(
                    response.get(
                        "error",
                        "Invalid credentials"
                    )
                )

    # =========================
    # REGISTER TAB
    # =========================

    with tab2:

        username = st.text_input(
            "Username",
            key="register_username"
        )

        password = st.text_input(
            "Password",
            type="password",
            key="register_password"
        )

        if st.button("Register"):

            response = register_user(
                username=username,
                password=password
            )

            if response.get("message"):

                st.success(
                    response["message"]
                )

            else:

                st.error(
                    response.get(
                        "error",
                        "Registration failed"
                    )
                )
