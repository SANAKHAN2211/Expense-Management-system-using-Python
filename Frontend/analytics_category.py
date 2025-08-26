import streamlit as st
from datetime import datetime
import requests

import pandas as pd

API_URL=  "http://localhost:8000"



def analytics_by_category():
    col1, col2 = st.columns(2)
    with col1:
           start_date=st.date_input("Start Date", datetime(2024,8,1))
    with col2:
           end_date=st.date_input("End Date", datetime(2024,9,1))

    if st.button("Get Analytics"):
        st.header("Expense Breakdown by Category")
        payload =  {
                "start_date": start_date.strftime("%Y-%m-%d"),
                "end_date": end_date.strftime("%Y-%m-%d")
        }

        response = requests.post(f"{API_URL}/analytics/", json=payload)
        response=response.json()



        data={
            "category":list(response.keys()),
            "total":[response[category]["total"] for category in response],
            "percentage": [response[category]["percentage"] for category in response]

        }


        df=pd.DataFrame(data=data)
        df_sorted = df.sort_values("percentage", ascending=False)


        st.bar_chart(data=df_sorted.set_index('category').sort_values("percentage", ascending=False),use_container_width=True)

        st.dataframe(df_sorted, hide_index=True)

