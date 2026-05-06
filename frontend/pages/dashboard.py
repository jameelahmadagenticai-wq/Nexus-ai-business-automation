import streamlit as st
import plotly.express as px
import pandas as pd

from api_client import get_health

st.title("NexusOS AI Dashboard")

st.markdown("Business Intelligence Overview")

# =========================
# KPI METRICS
# =========================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="Active Tasks",
        value="24",
        delta="+5"
    )

with col2:
    st.metric(
        label="Leads",
        value="128",
        delta="+12"
    )

with col3:
    st.metric(
        label="Emails Processed",
        value="342",
        delta="+48"
    )

with col4:
    st.metric(
        label="AI Queries",
        value="1,204",
        delta="+124"
    )

st.divider()

# =========================
# TASK ANALYTICS
# =========================

st.subheader("Task Analytics")

task_data = pd.DataFrame({
    "Day": [
        "Mon",
        "Tue",
        "Wed",
        "Thu",
        "Fri",
        "Sat",
        "Sun"
    ],
    "Tasks": [
        12,
        19,
        15,
        28,
        32,
        24,
        18
    ]
})

fig_tasks = px.line(
    task_data,
    x="Day",
    y="Tasks",
    markers=True,
    title="Tasks Completed This Week"
)

st.plotly_chart(
    fig_tasks,
    use_container_width=True
)

# =========================
# LEAD ANALYTICS
# =========================

st.subheader("Lead Pipeline")

lead_data = pd.DataFrame({
    "Stage": [
        "New",
        "Contacted",
        "Qualified",
        "Closed"
    ],
    "Count": [
        45,
        32,
        18,
        9
    ]
})

fig_leads = px.bar(
    lead_data,
    x="Stage",
    y="Count",
    title="CRM Lead Stages"
)

st.plotly_chart(
    fig_leads,
    use_container_width=True
)

# =========================
# SYSTEM STATUS
# =========================

st.subheader("System Status")

health = get_health()

status_col1, status_col2, status_col3 = st.columns(3)

with status_col1:
    if health.get("status") == "healthy":

        st.success("FastAPI Running")

    else:

        st.error(
            health.get(
                "error",
                "FastAPI unavailable"
            )
        )

with status_col2:
    st.success("PostgreSQL Connected")

with status_col3:
    st.success("Ollama Active")
