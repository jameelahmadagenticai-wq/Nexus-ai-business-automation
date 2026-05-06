import streamlit as st

from api_client import get_crm

st.title("CRM")

crm_status = get_crm()

if "error" in crm_status:

    st.error(crm_status["error"])

else:

    st.success(
        crm_status.get(
            "message",
            "CRM API connected"
        )
    )
