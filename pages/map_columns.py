import pandas as pd
import streamlit as st

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