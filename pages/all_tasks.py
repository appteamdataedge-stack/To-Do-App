"""Page 2 — All Tasks: Completed & Pending tabs with column-header filtering."""

import streamlit as st
import pandas as pd
from datetime import date
from db.queries import get_completed_tasks, get_pending_tasks
from st_aggrid import AgGrid, GridOptionsBuilder


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
    df["Deadline"] = df["Deadline"].astype(str)
    df = df[["Task Name", "Assigned To", "Create Date", "Deadline", "Over Due By"]]
    return df


def _show_grid(df: pd.DataFrame):
    """Render an AG Grid with sortable columns and click-to-filter on Task Name & Assigned To."""
    gb = GridOptionsBuilder.from_dataframe(df)

    # Default column: sortable, no filter
    gb.configure_default_column(sortable=True, filter=False, resizable=True)

    # Enable text filter popup on click for these two columns
    gb.configure_column("Task Name", filter="agTextColumnFilter")
    gb.configure_column("Assigned To", filter="agTextColumnFilter")

    grid_options = gb.build()

    AgGrid(
        df,
        gridOptions=grid_options,
        use_container_width=True,
        fit_columns_on_grid_load=True,
        # Show the filter icon in the header so users know they can click it
        enable_enterprise_modules=False,
    )


def render():
    st.header("All Tasks")

    tab_completed, tab_pending = st.tabs(["Completed Tasks", "Pending Tasks"])

    with tab_completed:
        df = _build_dataframe(get_completed_tasks())
        if df.empty:
            st.info("No completed tasks yet.")
        else:
            _show_grid(df)

    with tab_pending:
        df = _build_dataframe(get_pending_tasks())
        if df.empty:
            st.info("No pending tasks.")
        else:
            _show_grid(df)
