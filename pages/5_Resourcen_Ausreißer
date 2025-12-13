import streamlit as st
import pandas as pd
import pm4py
from Datenanalyse_Outlier import eventlog_to_image as eventlog_to_image
from Datenanalyse_Outlier import load_eventLog as load_eventLog
from streamlit_elements import elements, mui, nivo 
from Datenanalyse_Outlier.display_analysis.main import show_all_analysis
from Datenanalyse_Outlier.eventlog_to_dataframe import eventlog_to_df
from Datenanalyse_Outlier.map_columns import map_column

# --- SESSION STATE INITIALISIEREN ---
if "uploaded_logs" not in st.session_state or st.session_state["uploaded_logs"] is None:
    st.session_state["uploaded_logs"] = []

if not isinstance(st.session_state["uploaded_logs"], list):
    st.session_state["uploaded_logs"] = list(st.session_state["uploaded_logs"])

st.session_state.setdefault("latest_upload", None)
st.session_state.setdefault("file_path", None)
st.session_state.setdefault("file_type", None)
st.session_state.setdefault("file_name", None)
st.session_state.setdefault("df", None)
st.session_state.setdefault("log", None)
# Sonstige Session States für Ausreißer
st.session_state.setdefault("outlier_total", 0)
st.session_state.setdefault("outlier_checked", 0)  
st.session_state.setdefault("outliers_accepted", [])