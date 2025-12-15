
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
from streamlit_elements import elements, mui, nivo 
from Datenanalyse_Outlier.display_analysis.main import show_all_analysis
from Datenanalyse_Outlier.map_columns import map_column

#Session States für Ausreißer
st.session_state.setdefault("outlier_total", 0)
st.session_state.setdefault("outlier_checked", 0)  
st.session_state.setdefault("outliers_accepted", [])

st.title("🧭 Tabelle - Ausreißeranalyse")

# Prüfen, ob Datei vom Button-Code existiert
if "file_path" not in st.session_state or st.session_state["file_path"] is None:
    st.warning("⚠️ Bitte zuerst einen Eventlog auf der \"Upload Eventlog\" Seite hochladen.")
    st.stop()

# file_path = st.session_state["file_path"]
# file_type = st.session_state["file_type"]

# --- EVENTLOG EINLESEN ---
st.header("📄 Eventlog laden")
df = st.session_state["df"]
log = st.session_state["log"]


st.success("Eventlog erfolgreich geladen!")

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

st.subheader("📊 Prozentuale Gewichtung der Aktivität")

# Aktivitätsspalte automatisch erkennen 
activity_col = None
possible_cols = ["activity", "Activity", "concept:name", "task", "event", "event_name"]
total_events = len(df)

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
        {"activity": row[activity_col], "outliers": round(int(row["outliers"])/total_events * 100,2)}
        for _, row in stats.iterrows()
    ]

    # Anzeige der vorhandenen Daten
    # st.write("📊 Daten für Nivo-Chart:")
    # st.write(nivo_data)

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


# #############################################################
#  --- STATISTISCHE ANALYSE & AUSREISSER ---
st.subheader("📊 Statistische Analyse & Ausreißer")



  # Eventlog->Dataframe
if not isinstance(log, pd.DataFrame):
    # log_df = eventlog_to_df(log)
    log_df = pm4py.convert_to_dataframe(log)
else:
    log_df = log.copy()

# st.write(log_df.columns)
log_df = map_column(log_df)

log_df["timestamp"] = pd.to_datetime(log_df["timestamp"], errors="coerce")

log = log_df

show_all_analysis(log)

# Analysen durchführen und in Session state speichern 
from Datenanalyse_Outlier.show_analysis import show_all_analysis
st.session_state["outliers"] = show_all_analysis(log)