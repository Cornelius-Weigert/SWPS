import streamlit as st
import pandas as pd
import pm4py
from Datenanalyse_Outlier import eventlog_to_image as eventlog_to_image
from Datenanalyse_Outlier import load_eventLog as load_eventLog
from Datenanalyse_Outlier.display_analysis.outlier_resource import show_resource_outliers


# --- SESSION STATE INITIALISIEREN ---
if st.session_state.get("df") is None:
    st.warning("⚠️ Bitte zuerst einen Eventlog auf der \"Upload Eventlog\" Seite hochladen.")
    st.stop()

df = st.session_state.get("df")
log = st.session_state.get("log")

# Sonstige Session States für Ausreißer
outlier_total = st.session_state.get("outlier_total")
outlier_checked = st.session_state.get("outlier_checked")  
outliers_accepted = st.session_state.get("outliers_accepted")

show_resource_outliers(df)