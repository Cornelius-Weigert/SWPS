import streamlit as st
import tempfile
import Datenanalyse_Outlier.load_eventLog as load_eventLog
import Datenanalyse_Outlier.eventlog_to_image as eventlog_to_image
import pm4py
import pandas as pd
from Datenanalyse_Outlier.map_columns import map_column
from Datenanalyse_Outlier.display_analysis.frequency import show_frequency
from Datenanalyse_Outlier.display_analysis.duration_process import show_process_duration
from Datenanalyse_Outlier.display_analysis.resources import show_resources
from Datenanalyse_Outlier.display_analysis.duration_activity import show_activity_duration
from Datenanalyse_Outlier.display_analysis.standard_value import show_standard_compare
from Datenanalyse_Outlier.display_analysis.duration_process import show_process_duration

# --- SESSION STATE INITIALISIEREN ---
if "uploaded_logs" not in st.session_state or st.session_state["uploaded_logs"] is None:
    st.session_state["uploaded_logs"] = []

if not isinstance(st.session_state["uploaded_logs"], list):
    st.session_state["uploaded_logs"] = list(st.session_state["uploaded_logs"])

df = st.session_state.get("df")
log = st.session_state.get("log")

# Sonstige Session States für Ausreißer
outlier_total = st.session_state.get("outlier_total")
outlier_checked = st.session_state.get("outlier_checked")  
outliers_accepted = st.session_state.get("outliers_accepted")

tab1, tab2, tab3, tab4,tab5 = st.tabs([
    "Standardwerte-Vergleich",
    "Häufigkeit",
    "Prozessdauer",
    "Aktivitätsdauer",
    "Ressourcen",])

with tab1:
    show_standard_compare(df)
    
with tab2:
    show_frequency(df)

with tab3:
    show_process_duration(df)


with tab4:
    show_activity_duration(df)

with tab5:
    show_resources(df)