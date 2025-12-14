import streamlit as st
import pandas as pd


st.title("📑 Bericht - Ausreißeranalyse")

required_keys = [
    "df",
    "outlier_total",
    "outlier_checked",
    "outlier_accepted",
]

for key in required_keys:
    if key not in st.session_state:
        st.warning("Bitte zuerst Ausreißer-Analyse durchführen, bevor Bericht geladen werden kann")
        st.stop()

df = st.session_state["df"]

# Prüfen ob Outlier existieren
if "is_outlier" not in df.columns:
    st.info("Es wurden noch keine Ausreißer berechnet.")
    st.stop()

total_events = len(df)
total_outliers = st.session_state["outlier_total"]
checked_outliers = st.session_state["outlier_checked"]
outliers_accepted = st.session_state["outliers_accepted"]

ratio = (total_outliers / total_events * 100) if total_events > 0 else 0

# --- KPI ---
c1, c2, c3 = st.columns(3)
c1.metric("Events", total_events)
c2.metric("Ausreißer", total_outliers)
c3.metric("Anteil", f"{ratio:.2f} %")

st.markdown("---")

# --- Outlier-Tabelle ---
st.subheader("📌 Detektierte Ausreißer")
outlier_df = df[df["is_outlier"] == True]

if len(outlier_df) == 0:
    st.success("Keine Ausreißer gefunden 🎉")
else:
    st.dataframe(outlier_df, width="stretch")

    # CSV Export
    csv = outlier_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        "📥 Ausreißer als CSV herunterladen",
        csv,
        "outliers.csv",
        "text/csv"
    )
