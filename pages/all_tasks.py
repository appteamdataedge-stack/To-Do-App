"""Page 2 — All Tasks: Completed & Pending tabs with sortable/searchable tables."""

import streamlit as st
import pandas as pd
from datetime import date
from db.queries import get_completed_tasks, get_pending_tasks


def _build_dataframe(tasks: list[dict]) -> pd.DataFrame:
    """Convert task list to a display-ready DataFrame with 'Over Due By' column."""
    if not tasks:
        return pd.DataFrame()

    df = pd.DataFrame(tasks)
    df = df.rename(columns={
        "task_name": "Task Name",
        "assigned_to": "Assigned To",
        "created_at": "Create Date",
        "deadline": "Deadline",
    })

    today = date.today()
    df["Over Due By"] = df["Deadline"].apply(
        lambda d: f"{(today - d).days} days" if today > d else "0 days"
    )
    df["Create Date"] = pd.to_datetime(df["Create Date"]).dt.strftime("%Y-%m-%d")
    df = df[["Task Name", "Assigned To", "Create Date", "Deadline", "Over Due By"]]
    return df


def render():
    st.header("All Tasks")

    tab_completed, tab_pending = st.tabs(["Completed Tasks", "Pending Tasks"])

    with tab_completed:
        df = _build_dataframe(get_completed_tasks())
        if df.empty:
            st.info("No completed tasks yet.")
        else:
            st.dataframe(df, use_container_width=True, hide_index=True)

    with tab_pending:
        df = _build_dataframe(get_pending_tasks())
        if df.empty:
            st.info("No pending tasks.")
        else:
            st.dataframe(df, use_container_width=True, hide_index=True)
