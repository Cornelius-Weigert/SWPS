import streamlit as st
import pandas as pd

def accept_outliers(selected_rows, category,outlier_df):
    if st.session_state.get("outliers_accepted") is None:
        st.session_state["outliers_accepted"] = []
    filtered_outlier_df = outlier_df.iloc[selected_rows]
    st.session_state["outliers_accepted"].append([category, filtered_outlier_df])
    st.success(f"✅ {len(filtered_outlier_df)} Ausreißer in der Kategorie '{category}' wurden akzeptiert.")