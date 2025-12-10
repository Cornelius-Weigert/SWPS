import streamlit as st
import pandas as pd
#from analyse_modul import detect_outliers_custom  # dein Teamkollegen-Modul

# --- SESSION STATE INITIALISIEREN ---
if "uploaded_logs" not in st.session_state or st.session_state["uploaded_logs"] is None:
    st.session_state["uploaded_logs"] = []

if not isinstance(st.session_state["uploaded_logs"], list):
    st.session_state["uploaded_logs"] = list(st.session_state["uploaded_logs"])

st.session_state.setdefault("latest_upload", None)
st.session_state.setdefault("file_path", None)
st.session_state.setdefault("file_type", None)
st.session_state.setdefault("file_name", None)

st.set_page_config(page_title="Ausreißer Analyse", layout="wide")
st.title("🔍 Ausreißer Analyse")

# --- 1️⃣ Datei-Upload ---
uploaded_file = st.file_uploader("Bitte Datensatz hochladen (XES oderCSV)", type=["xes", "csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.success("✅ Datei erfolgreich geladen!")
    st.write("**Vorschau des Datensatzes:**")
    st.dataframe(df.head())

    # --- 2️⃣ Nutzer fragen, ob Ausreißeranalyse gewünscht ist ---
    st.subheader("Ausreißeranalyse konfigurieren")
    analyse_ausreisser = st.radio(
        "Möchten Sie den Datensatz auf Ausreißer prüfen?",
        options=["Nein", "Ja"],
        horizontal=True
    )

    if analyse_ausreisser == "Ja":
        # --- 3️⃣ Auswahl: Gesamter Datensatz oder bestimmtes Feature ---
        modus = st.radio(
            "Welche Daten sollen analysiert werden?",
            options=["Gesamter Datensatz", "Nur bestimmtes Feature"]
        )

        # Wenn nur bestimmtes Feature
        spalte = None
        if modus == "Nur bestimmtes Feature":
            spalte = st.selectbox(
                "Bitte Spalte auswählen:", 
                options=df.columns.tolist()
            )

        # --- 4️⃣ Ausreißer erkennen (mit dem Modul deines Kollegen) ---
        with st.spinner("Analysiere Daten..."):
            ausreisser_df = detect_outliers_custom(df)

        if ausreisser_df.empty:
            st.info("Keine Ausreißer gefunden.")
        else:
            # Wenn bestimmtes Feature gewählt wurde, darauf filtern
            if spalte:
                ausreisser_df = ausreisser_df[ausreisser_df["Spalte"] == spalte]

            st.subheader("Erkannte Ausreißer")
            st.dataframe(ausreisser_df, use_container_width=True)

            # --- 5️⃣ Optional: Gefilterte Daten herunterladen ---
            csv = ausreisser_df.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="📥 Gefilterte Ausreißer herunterladen (CSV)",
                data=csv,
                file_name="ausreisser_ergebnisse.csv",
                mime="text/csv"
            )

    else:
        st.info("Es wird keine Ausreißeranalyse durchgeführt.")
