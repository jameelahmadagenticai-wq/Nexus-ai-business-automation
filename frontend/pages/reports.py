import streamlit as st

from api_client import get_reports

st.title("Reports")

reports_status = get_reports()

if "error" in reports_status:

    st.error(reports_status["error"])

else:

    st.success(
        reports_status.get(
            "message",
            "Reports API connected"
        )
    )
