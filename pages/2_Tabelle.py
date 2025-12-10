
#kompatibel mit button.py: hochladen einer Datei in button.py lässt tabelle1 erst laden!
import sys, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ROOT)
print("UPDATED SYSPATH:", sys.path)

import streamlit as st
import pandas as pd
import pm4py
from Datenanalyse_Outlier import eventlog_to_image as eventlog_to_image
from Datenanalyse_Outlier import load_eventLog as load_eventLog
# from pages.map_columns import map_column
from streamlit_elements import elements, mui, nivo 


# --- SESSION STATE INITIALISIEREN ---
if "uploaded_logs" not in st.session_state or st.session_state["uploaded_logs"] is None:
    st.session_state["uploaded_logs"] = []

if not isinstance(st.session_state["uploaded_logs"], list):
    st.session_state["uploaded_logs"] = list(st.session_state["uploaded_logs"])

st.session_state.setdefault("latest_upload", None)
st.session_state.setdefault("file_path", None)
st.session_state.setdefault("file_type", None)
st.session_state.setdefault("file_name", None)

st.title("🧭 Tabelle - Ausreißeranalyse")

# Prüfen, ob Datei vom Button-Code existiert
if "file_path" not in st.session_state or st.session_state["file_path"] is None:
    st.warning("⚠️ Bitte zuerst einen Eventlog auf der Button-Seite hochladen.")
    st.stop()

file_path = st.session_state["file_path"]
file_type = st.session_state["file_type"]

# --- EVENTLOG EINLESEN ---
st.header("📄 Eventlog laden")

# '''
def map_column(df):
    # Kleinbuchstaben
    df.columns = [c.lower() for c in df.columns]

    # Mapping für notwendige Spalten
    col_map = {}

    # case_id-Spalte
    for name in ["case_id", "case", "Case_ID", "Case ID", "Case_id", "case id", "case:concept:name","id","ID", "case ID"]:
        if name in df.columns:
            col_map[name] = "case_id"
            break

    # activity-Spalte
    for name in ["activity", "Activity", "concept_name", "concept:name"]:
        if name in df.columns:
            col_map[name] = "activity"
            break

    # timestamp-Spalte
    for name in ["timestamp", "Complete Timestamp", "Complete timestamp", "complete timestamp", "Timestamp", "time", "time:timestamp"]:
        if name in df.columns:
            col_map[name] = "timestamp"
            break

    # Resource-Spalte
    for name in ["org:resource","resource"]:
        if name in df.columns:
            col_map[name] = "resource"
            break   

    df = df.rename(columns=col_map)
    
    # Prüfen, ob alle Pflichtspalten jetzt existieren
    must_have = {"case_id", "activity", "timestamp"}
    if not must_have.issubset(df.columns):
        missing = must_have - set(df.columns)
        st.error(f"❌ CSV benötigt die Spalten: {', '.join(missing)}")
        st.stop()

    # Timestamp konvertieren
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors='coerce')
    if df["timestamp"].isnull().all():
        st.error("❌ Konnte keine gültigen Zeitstempel erkennen.")
        st.stop()
              
    return df
# '''

# df = map_column(df)

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

st.success("Eventlog erfolgreich geladen!")

# --- TABELLENVORSCHAU ---
st.subheader("📋 Interaktive Tabellen-Vorschau")
st.dataframe(df.head(30), width='stretch')

st.markdown("---")

# --- AUSREISSER-COUNTER ---
if "is_outlier" in df.columns:
    total_outliers = df["is_outlier"].sum()
    checked_outliers = df["is_outlier_checked"].sum() if "is_outlier_checked" in df.columns else 0

    col1, col2 = st.columns(2)
    col1.metric("Gesamt Ausreißer", total_outliers)
    col2.metric("Überprüfte Ausreißer", checked_outliers)
else:
    st.info("Keine Ausreißer-Spalte gefunden. Counter wird aktualisiert, sobald die Logik hinzugefügt wird.")

# --- Nivo-Chart ---

st.subheader("📊 Chart: Anzahl Outlier pro Aktivität")

# Aktivitätsspalte automatisch erkennen 
activity_col = None
possible_cols = ["activity", "Activity", "concept:name", "task", "event", "event_name"]

for col in df.columns:
    if col.lower() in possible_cols:
        activity_col = col
        break

if activity_col is None:
    st.warning(
        "⚠️ Es wurde keine Aktivitätsspalte gefunden. "
        "Erwartet wird z.B. 'Activity', 'activity', 'concept:name', ..."
    )
else:
    # Anzahl Outlier pro Aktivität berechnen
    if "is_outlier" in df.columns:
        stats = (
            df.groupby(activity_col)["is_outlier"]
            .sum()
            .reset_index()
            .rename(columns={"is_outlier": "outliers"})
        )
    else:
        stats = df.groupby(activity_col).size().reset_index(name="outliers")

    # Daten für Nivo formatieren
    nivo_data = [
        {"activity": row[activity_col], "outliers": int(row["outliers"])}
        for _, row in stats.iterrows()
    ]

    # Anzeige der vorhandenen Daten
    st.write("📊 Daten für Nivo-Chart:")
    st.write(nivo_data)

    # Nivo Radar Chart anzeigen
    with elements("nivo_outlier_chart"):
        with mui.Box(sx={"height": 500}):
            nivo.Radar(
                data=nivo_data,
                keys=["outliers"],
                indexBy="activity",
                margin={"top": 70, "right": 80, "bottom": 40, "left": 80},
                dotSize=8,
                motionConfig="gentle",
            )



# --- SESSION STATE ---
st.session_state.setdefault("df", None)
st.session_state.setdefault("outlier_total", 0)
st.session_state.setdefault("outlier_checked", 0)  
