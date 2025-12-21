import streamlit as st
import pandas as pd
from io import StringIO


st.title("📑 Bericht - Ausreißeranalyse")

required_keys = [
    "df",
    "outlier_total",
    "outlier_checked",
    "outlier_accepted",
]

st.button("Bericht zurücksetzen", on_click=lambda:st.session_state["outliers_accepted"].clear())
# for key in required_keys:
#     if key not in st.session_state:
#         st.warning("Bitte zuerst Ausreißer-Analyse durchführen, bevor Bericht geladen werden kann")
#         st.stop()

# Sicherheitscheck für df (falls leer)
df = st.session_state.get("df")
if df is None:
    st.warning("Bitte zuerst Ausreißeranalyse durchführen!")
    st.stop()

# Sicherheitscheck für outliers (falls leer)
outliers = st.session_state.get("outliers_accepted",[])
if not outliers:
    st.info("Es wurden noch keine Ausreißer für den Bericht ausgewählt!")
    st.stop()

# To Do: outliers nach Kategorie gruppieren
for idx, i in enumerate(outliers):
    st.write("---")
    category = i[0]
    st.subheader(f"Akzeptierte Ausreißer - {category}")
    st.dataframe(i[1],
                width="stretch",
                hide_index=True,)

    # Kommentar Funktion zu jeder Kategorie
    comment = st.text_area(
    "Kommentar zu dieser Kategorie",
    value = st.session_state.get(f"comment_{idx}",""),
    key = f"comment_{idx}",
    height=100
    )

    # CSV für Kategorie inklusive Kommentar
    csv_buffer = StringIO()
    df_with_comment = df.copy()
    df_with_comment["Kommentar"] = comment
    df_with_comment.to_csv(csv_buffer, index=False)

    # Download Funktion mit Kommentarspalte
    st.download_button(
    label="Tabelle herunterladen",
    data=csv_buffer.getvalue(),
    file_name=f"bericht_{category}.csv",
    mime="text/csv",
    key=f"download_{idx}"
    )    