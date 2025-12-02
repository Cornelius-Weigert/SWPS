import streamlit as st
import os
import tempfile
import Datenanalyse_Outlier.load_eventLog as load_eventLog
import Datenanalyse_Outlier.eventlog_to_image as eventlog_to_image
from pages.map_columns import map_column
import pm4py
import pandas as pd

# --- Upload Funktion ---
def upload_eventlog():
    uploaded_file = st.file_uploader(
        "Datei auswählen", 
        type=["xes", "csv"], 
        key="eventlog_uploader"
    )
    if uploaded_file is not None:

        # Temporäre Datei sichern
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp_file:
            tmp_file.write(uploaded_file.read())
            file_path = tmp_file.name

        extension = os.path.splitext(uploaded_file.name)[1].lower()
        file_type = "XES" if extension == ".xes" else "CSV"

        # Speichern in Session-State
        st.session_state["file_path"] = file_path
        st.session_state["file_type"] = file_type
        st.session_state["file_name"] = uploaded_file.name

        st.success(f"Datei erfolgreich hochgeladen: {uploaded_file.name} ({file_type})")

# --- UI ---
st.title("Eventlog hochladen")

st.write("Bitte Eventlog hochladen (XES oder CSV):")

# Upload immer anzeigen (damit neue Datei geladen werden kann)
upload_eventlog()

file_path = st.session_state["file_path"]
file_type = st.session_state["file_type"]

try:
    if file_type == "CSV":
        df = pd.read_csv(file_path)
        df = map_column(df)
        log = load_eventLog.eventLog_from_csv(file_path)

    elif file_type == "XES":
        log = pm4py.read_xes(file_path)
        df = pm4py.convert_to_dataframe(log)
        df = map_column(df)
        log = load_eventLog.eventLog_from_xes(file_path)

    else:
        st.error("❌ Unbekanntes Dateiformat.")
        st.stop()

except Exception as e:
    st.error(f"❌ Fehler beim Einlesen der Datei: {e}")
    st.stop()


# --- STATISTIKEN ---
st.subheader("📊 Log-Statistiken")

num_cases = df["case_id"].nunique()
num_events = len(df)
num_activities = df["activity"].nunique()
timespan = df["timestamp"].max() - df["timestamp"].min()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Cases", num_cases)
col2.metric("Events", num_events)
col3.metric("Activities", num_activities)
col4.metric("Period", str(timespan))

st.markdown("---")

# --- DIRECTLY-FOLLOWS GRAPH ---
st.subheader("🔁 Directly-Follows Graph (DFG)")

percentage_slider = st.slider("Prozentsatz der häufigsten Pfade anzeigen (%)", min_value=5, max_value=100, value=20, step=5)/100
st.image(eventlog_to_image.get_dfg_image(log,percentage=percentage_slider))
st.markdown("---")

# --- HÄUFIGSTE AKTIVITÄTEN ---
st.subheader("🔥 Häufigste Aktivitäten")
st.bar_chart(df["activity"].value_counts())