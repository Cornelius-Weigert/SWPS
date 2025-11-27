
#kompatibel mit button.py: hochladen einer Datei in button.py lässt tabelle1 erst laden!


import streamlit as st
import pandas as pd
import pm4py

st.title("🧭 Process-Mining Preview")

# Prüfen, ob Datei vom Button-Code existiert
if "file_path" not in st.session_state or st.session_state["file_path"] is None:
    st.warning("⚠️ Bitte zuerst einen Eventlog auf der Button-Seite hochladen.")
    st.stop()

file_path = st.session_state["file_path"]
file_type = st.session_state["file_type"]

# --- EVENTLOG EINLESEN ---
st.header("📄 Eventlog laden")

def map_columns(df):
    # Kleinbuchstaben
    df.columns = [c.lower() for c in df.columns]

    # Mapping für notwendige Spalten
    col_map = {}

    # case_id-Spalte
    for name in ["case_id", "case", "Case_ID", "Case ID", "Case_id", "case id", "case:concept:name"]:
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

try:
    if file_type == "CSV":
        df = pd.read_csv(file_path)
        df = map_columns(df)

    elif file_type == "XES":
        log = pm4py.read_xes(file_path)
        df = pm4py.convert_to_dataframe(log)
        df = map_columns(df)

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

# --- HÄUFIGSTE AKTIVITÄTEN ---
st.subheader("🔥 Häufigste Aktivitäten")
st.bar_chart(df["activity"].value_counts())

st.markdown("---")

# --- DIRECTLY-FOLLOWS GRAPH ---          muss mit Cornelius seinem Code vllt zusammengeführt werden ?
st.subheader("🔁 Directly-Follows Graph (DFG)")

df_sorted = df.sort_values(["case_id", "timestamp"])
transitions = []

for case in df_sorted["case_id"].unique():
    events = df_sorted[df_sorted["case_id"] == case]["activity"].tolist()
    transitions.extend(list(zip(events, events[1:])))

dfg_df = pd.DataFrame(transitions, columns=["Von", "Nach"])
st.dataframe(dfg_df, width='stretch')


# komischer KeyError, muss noch behoben werden (wahrscheinlich wegen dem code in button.py)