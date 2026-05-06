import streamlit as st

from api_client import stream_chat_message

st.title("NexusOS AI Chat")

# =========================
# SESSION STATE
# =========================

if "messages" not in st.session_state:
    st.session_state.messages = []

# =========================
# DISPLAY OLD MESSAGES
# =========================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# =========================
# USER INPUT
# =========================

prompt = st.chat_input("Ask NexusOS AI...")

if prompt:

    history = st.session_state.messages.copy()

    # Save user message
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    # Show user message
    with st.chat_message("user"):
        st.markdown(prompt)

    assistant_index = len(st.session_state.messages)

    st.session_state.messages.append({
        "role": "assistant",
        "content": ""
    })

    # =========================
    # API CALL
    # =========================

    full_response = ""

    with st.chat_message("assistant"):

        response_container = st.empty()

        for chunk in stream_chat_message(
            prompt,
            history=history
        ):

            full_response += chunk

            st.session_state.messages[assistant_index]["content"] = (
                full_response
            )

            response_container.markdown(full_response)

    if not full_response:

        full_response = "Error: empty response from backend"

        st.session_state.messages[assistant_index]["content"] = (
            full_response
        )

        response_container.markdown(full_response)
