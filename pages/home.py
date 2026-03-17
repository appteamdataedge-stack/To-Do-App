"""Page 1 — Home: Active tasks + Add Task form."""

import streamlit as st
from datetime import date, timedelta
from db.queries import add_task, get_pending_tasks, mark_task_done


def render():
    st.header("Home — Active Tasks")

    # --- Add Task Form ---
    st.subheader("Add New Task")
    with st.form("add_task_form", clear_on_submit=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            task_name = st.text_input("Task Name")
        with col2:
            assigned_to = st.text_input("Assigned To")
        with col3:
            deadline = st.date_input("Deadline", value=date.today() + timedelta(days=7))
        submitted = st.form_submit_button("Save Task")

        if submitted:
            if not task_name.strip() or not assigned_to.strip():
                st.error("Task Name and Assigned To are required.")
            else:
                add_task(task_name.strip(), assigned_to.strip(), deadline)
                st.success(f"Task '{task_name}' added!")
                st.rerun()

    # --- Active Task List ---
    st.divider()
    st.subheader("Pending Tasks")

    tasks = get_pending_tasks()
    if not tasks:
        st.info("No pending tasks. Add one above!")
        return

    for task in tasks:
        col_check, col_name = st.columns([0.5, 9.5])
        with col_check:
            if st.checkbox("", key=f"done_{task['id']}", label_visibility="collapsed"):
                mark_task_done(task["id"])
                st.rerun()
        with col_name:
            st.write(f"**{task['task_name']}** — assigned to *{task['assigned_to']}* · due {task['deadline']}")
