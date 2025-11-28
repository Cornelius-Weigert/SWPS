import streamlit as st
from statistic_analysis import (
    outlier_case_duration,
    outlier_activity_duration,
    outlier_numeric,
    time_analysis,
    duration
)

def show_outliers(log):

    st.subheader("❗️ Ausreißer - Case Duration")

    durations = time_analysis.time_analysis1(log)
    if durations is not None:
        outliers_case, bounds_case = outlier_case_duration.case_duration_outliers(durations)
        st.write(f"Schwellenwerte (Sekunden): {bounds_case}")
        st.dataframe(outliers_case, use_container_width=True)
    else:
        st.info("Keine Zeitdaten - Case Duration Outliers übersprungen.")

    st.subheader("❗️Ausreißer - Activity Duration")

    activity_df = duration.duration_pro_activity(log)
    if activity_df is not None:
        outliers_activity, bounds_activity = outlier_activity_duration.activity_duration_outliers(activity_df)
        st.write(f"Schwellenwerte (Sekunden): {bounds_activity}")
        st.dataframe(outliers_activity, use_container_width=True)
    else:
        st.info("Keine Aktivitätsdauer - Activity Outliers übersprungen.")

    st.subheader("❗️Ausreißer - Numerische Werte")

    numeric_cols = log.select_dtypes(include="number").columns

    if len(numeric_cols) == 0:
        st.info("Keine numerischen Spalten - Numeric Outliers übersprungen.")
        return

    # users can choose the column of numeric analysis
    selected_numeric = st.selectbox(
        "Numerische Spalte wählen:",
        numeric_cols
    )

    outliers_numeric, bounds_numeric = outlier_numeric.numeric_outliers(log1, selected_numeric)
    st.write(f"Schwellenwerte: {bounds_numeric}")
    st.dataframe(outliers_numeric, use_container_width=True)
