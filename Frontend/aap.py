import streamlit as st
from Frontend.add_update_ui import add_update_tab
from Frontend.analytics_category import analytics_by_category
from Frontend.analytics_months import analytics_by_months

API_URL="http://localhost:8000"

st.title("Expense Management System")
tab1,tab2,tab3=st.tabs(["Add/Updates","Analytics by Category","Analytics by Months"])

with tab1:
    add_update_tab()

with tab2:
    analytics_by_category()
with tab3:
    analytics_by_months()
