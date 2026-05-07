import streamlit as st
import requests


st.title("📧 NexusOS Email Dashboard")


# =========================
# FETCH EMAILS
# =========================

response = requests.get(
    "http://localhost:8000/dashboard/emails"
)

emails = response.json()


# =========================
# EMAIL LIST
# =========================

for idx, email in enumerate(emails):

    with st.expander(
        f"{email['subject']}"
    ):

        st.write(
            f"Sender: {email['sender']}"
        )

        st.write("### Original Email")

        st.write(email["body"])

        st.write("### AI Draft Reply")

        st.code(email["draft_reply"])

        status = (
            "✅ Approved"
            if email["approved"]
            else "⏳ Pending Approval"
        )

        st.write(f"Status: {status}")

        # =========================
        # APPROVAL BUTTON
        # =========================

        if not email["approved"]:

            if st.button(
                f"Approve & Send #{idx}"
            ):

                send_response = requests.post(
                    "http://localhost:8000/email/send",
                    json={
                        "recipient": email["sender"],
                        "subject": f"Re: {email['subject']}",
                        "body": email["draft_reply"]
                    }
                )

                if send_response.status_code == 200:

                    email["approved"] = True

                    st.success(
                        "Email sent successfully"
                    )