import streamlit as st
import pandas as pd
from streamlit_elements import elements, mui, nivo

# ---------------------------------------------------------
# 1) Outlier-Erkennung (muss noch mit Yaxin ihren Code getauscht werden!)
# ---------------------------------------------------------
def detect_columns(df):
    cols = df.columns

    # Ergebnisse
    detected = {
        "case_id": None,
        "activity": None,
        "timestamp": None,
        "numeric": []
    }

    # Kandidatenlisten

    case_candidates = [
        "case", "caseid", "case_id", "case-id",
        "trace", "traceid", "trace_id",
        "case:concept:name", "trace:concept:name"
    ]

    activity_candidates = [
        "activity", "event", "event_name", "event name",
        "concept:name", "task", "operation"
    ]

    time_candidates = [
        "time", "timestamp", "time:timestamp",
        "complete timestamp", "start time", "end time", "event_time"
    ]

    # 1) Exact matching -----------------------------------------
    for col in cols:
        # Case-ID
        if col in case_candidates:
            detected["case_id"] = col

        # Activity
        if col in activity_candidates:
            detected["activity"] = col

        # Timestamp
        if col in time_candidates:
            detected["timestamp"] = col

    # 2) Case-insensitive matching ------------------------------
    for col in cols:
        low = col.lower()

        # Case-ID
        if any(low == c.lower() for c in case_candidates) and not detected["case_id"]:
            detected["case_id"] = col

        # Activity
        if any(low == c.lower() for c in activity_candidates) and not detected["activity"]:
            detected["activity"] = col

        # Timestamp
        if any(low == c.lower() for c in time_candidates) and not detected["timestamp"]:
            detected["timestamp"] = col

    # 3) Fuzzy matching -----------------------------------------
    for col in cols:
        low = col.lower()

        if detected["case_id"] is None and ("case" in low or "trace" in low):
            detected["case_id"] = col

        if detected["activity"] is None and ("act" in low or "event" in low or "concept:name" in low):
            detected["activity"] = col

        if detected["timestamp"] is None and ("time" in low or "stamp" in low):
            detected["timestamp"] = col

    # 4) Numeric / float columns for Outliers --------------------
    for col in cols:
        if df[col].dtype in ["float64", "int64"]:
            detected["numeric"].append(col)

    return detected

#---------------------------------------------------------

# Streamlit Seite

st.title("Eventlog Analyse mit Outlier-Erkennung & Nivo-Charts")


# 2) Datei-Upload

uploaded = st.file_uploader("Bitte Eventlog hochladen", type=["csv", "xes"])
if uploaded is not None:
 
 st.success(f" Datei erfolgreich hochgeladen!")

if uploaded:
    # CSV Beispiel
    df = pd.read_csv(uploaded)

    st.subheader("📄 Vorschau des Datensatzes")
    st.dataframe(df.head())

    
    # 3) Filter-Optionen

    st.subheader("⚙️ Einstellungen")

    apply_outlier_filter = st.checkbox("Outlier-Erkennung durchführen?")

    # Falls Outlier-Filter aktiviert wird → Spalte wählen
    if apply_outlier_filter:
        numeric_cols = df.select_dtypes(include=["int64", "float64"]).columns
        selected_col = st.selectbox(
            "Spalte für Outlier-Erkennung auswählen",
            numeric_cols
        )

        df = detect_columns(df, selected_col)

        # Auswahl: auf ganze Datei filtern oder nur bestimmte Werte
        filter_option = st.selectbox(
            "Wie möchtest du filtern?",
            ["Gesamte Datei filtern", "Nur Outlier anzeigen", "Nur normale Werte anzeigen"]
        )

        if filter_option == "Nur Outlier anzeigen":
            df = df[df["is_outlier"] == True]

        elif filter_option == "Nur normale Werte anzeigen":
            df = df[df["is_outlier"] == False]

    
    # 4) Chart-Daten vorbereiten
    
    st.subheader("📊 Chart: Anzahl Outlier pro Aktivität")

    if "Activity" in df.columns:
        # Anzahl Outlier pro Aktivität
        if "is_outlier" in df.columns:
            stats = (
                df.groupby("Activity")["is_outlier"]
                .sum()
                .reset_index()
                .rename(columns={"is_outlier": "outliers"})
            )
        else:
            # Falls Outlier nicht aktiviert → trotzdem etwas anzeigen
            stats = df.groupby("Activity").size().reset_index(name="outliers")

        # Format für Nivo:
        nivo_data = [
            {"activity": row["Activity"], "outliers": int(row["outliers"])}
            for i, row in stats.iterrows()
        ]

        # Debug-Ausgabe
        st.write("Daten für Nivo-Chart:")
        st.write(nivo_data)

        
        # 5) Nivo Radar Chart
        
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

    else:
        st.warning("Spalte 'activity' nicht gefunden – bitte sicherstellen, dass dein Eventlog Aktivitäten enthält.")