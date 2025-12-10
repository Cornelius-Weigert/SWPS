import streamlit as st
import pandas as pd
import numpy as np
import io

st.set_page_config(page_title="Ausreißer Analyse", layout="wide")

st.title("🔍 Ausreißer Analyse")

# --- Schritt 1: Datei-Upload ---
uploaded_file = st.file_uploader("Bitte Datensatz hochladen (CSV)", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.success("✅ Datei erfolgreich geladen!")
    st.write("**Vorschau des Datensatzes:**")
    st.dataframe(df.head())

    # --- Schritt 2: Ausreißer-Erkennung (z.B. Z-Score Methode) ---
    def detect_outliers(df, z_thresh=2.5):
        outliers = []
        for col in df.select_dtypes(include=np.number).columns:
            mean = df[col].mean()
            std = df[col].std()
            z_scores = (df[col] - mean) / std
            col_outliers = df.loc[z_scores.abs() > z_thresh, [col]].copy()
            col_outliers["Spalte"] = col
            col_outliers["Z-Score"] = z_scores[z_scores.abs() > z_thresh]
            col_outliers["Typ"] = np.where(col_outliers["Z-Score"] > 0, "positiver Ausreißer", "negativer Ausreißer")
            outliers.append(col_outliers)
        if outliers:
            return pd.concat(outliers).reset_index().rename(columns={"index": "Zeile"})
        else:
            return pd.DataFrame(columns=["Zeile", "Spalte", "Wert", "Z-Score", "Typ"])

    ausreißer_df = detect_outliers(df)

    # --- Schritt 3: Filtermöglichkeiten ---
    st.subheader("Filter für Ausreißer")
    spalten = sorted(ausreißer_df["Spalte"].unique())
    typ_filter = st.multiselect("Typ auswählen", options=["positiver Ausreißer", "negativer Ausreißer"], default=["positiver Ausreißer", "negativer Ausreißer"])
    spalte_filter = st.multiselect("Spalte auswählen", options=spalten, default=spalten)

    gefiltert = ausreißer_df[
        ausreißer_df["Spalte"].isin(spalte_filter) &
        ausreißer_df["Typ"].isin(typ_filter)
    ]

    # --- Schritt 4: Tabelle anzeigen ---
    st.subheader("Erkannte Ausreißer")
    if not gefiltert.empty:
        st.dataframe(gefiltert, use_container_width=True)
    else:
        st.info("Keine Ausreißer nach den gewählten Kriterien gefunden.")

    # --- Schritt 5: Bewertung (z. B. über Checkboxen oder Bewertungsspalte) ---
    st.subheader("Bewertung der Ausreißer")
    bewertungen = st.text_input("Kommentar oder Bewertung eingeben (optional)")

    # --- Schritt 6: Download ---
    csv = gefiltert.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Gefilterte Ausreißer herunterladen (CSV)",
        data=csv,
        file_name="ausreisser_analyse.csv",
        mime="text/csv"
    )

else:
    st.info("Bitte zuerst eine CSV-Datei hochladen, um mit der Analyse zu starten.")
