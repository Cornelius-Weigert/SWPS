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

# # Prüfen ob Outlier existieren
# if "is_outlier" not in df.columns:
#     st.info("Es wurden noch keine Ausreißer berechnet.")
#     st.stop()

# total_events = len(df)
# total_outliers = st.session_state["outlier_total"]
# checked_outliers = st.session_state["outlier_checked"]
# outliers_accepted = st.session_state["outliers_accepted"]

# ratio = (total_outliers / total_events * 100) if total_events > 0 else 0

# # --- KPI ---
# c1, c2, c3 = st.columns(3)
# c1.metric("Events", total_events)
# c2.metric("Ausreißer", total_outliers)
# c3.metric("Anteil", f"{ratio:.2f} %")

# st.markdown("---")

# # --- Outlier-Tabelle ---
# st.subheader("📌 Detektierte Ausreißer")
# outlier_df = df[df["is_outlier"] == True]

# if len(outlier_df) == 0:
#     st.success("Keine Ausreißer gefunden 🎉")
# else:
#     st.dataframe(outlier_df, width="stretch")

#     # CSV Export
#     csv = outlier_df.to_csv(index=False).encode("utf-8")
#     st.download_button(
#         "📥 Ausreißer als CSV herunterladen",
#         csv,
#         "outliers.csv",
#         "text/csv"
#     )
