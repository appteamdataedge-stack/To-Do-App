"""Streamlit entry point — To-Do App with page routing."""

import streamlit as st

st.set_page_config(page_title="To-Do App", page_icon="📋", layout="wide")

page = st.sidebar.radio("Navigate", ["Home", "All Tasks"])

if page == "Home":
    from pages.home import render
    render()
else:
    from pages.all_tasks import render
    render()
