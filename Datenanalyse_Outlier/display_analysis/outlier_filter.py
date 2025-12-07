import streamlit as st
from statistic_analysis import (
    outlier_case_duration,
    outlier_activity_duration,
    outlier_numeric,
    time_analysis,
    duration
)
def show_outliers(log):

    st.subheader("❗️ Filter - Case Duration")
#
    durations = time_analysis.time_analysis1(log)
    if durations is not None:
        st.write("### Quantile Einstellungen für Case Duration")
        lower_case = st.slider("Unteres Quantil (Case)", 0.0, 0.5, 0.10, 0.01)
        upper_case = st.slider("Oberes Quantil (Case)", 0.5, 1.0, 0.90, 0.01)
        factor_case = st.slider("IQR-Faktor (Case)", 1.0, 5.0, 1.5, 0.1)

        outliers_case, bounds_case = outlier_case_duration.case_duration_outliers(
            durations, lower1=lower_case, upper1=upper_case, factor=factor_case
        )
        st.write(f"Schwellenwerte (Sekunden): {bounds_case}")
        st.dataframe(outliers_case, use_container_width=True)
    else:
        st.info("Keine Zeitdaten - Case Duration Outliers übersprungen.")

    st.subheader("❗️ Filter - Activity Duration")

    activity_df = duration.duration_pro_activity(log)
    if activity_df is not None:
        st.write("### Quantile Einstellungen für Activity Duration")
        lower_act = st.slider("Unteres Quantil (Activity)", 0.0, 0.5, 0.10, 0.01)
        upper_act = st.slider("Oberes Quantil (Activity)", 0.5, 1.0, 0.90, 0.01)
        factor_act = st.slider("IQR-Faktor (Activity)", 1.0, 5.0, 1.5, 0.1)

        outliers_activity, bounds_activity = outlier_activity_duration.activity_duration_outliers(
            activity_df, lower1=lower_act, upper1=upper_act, factor=factor_act
        )
        st.write(f"Schwellenwerte (Sekunden): {bounds_activity}")
        st.dataframe(outliers_activity, use_container_width=True)
    else:
        st.info("Keine Aktivitätsdauer - Activity Outliers übersprungen.")

    st.subheader("❗️ Filter - Numerische Werte")

    numeric_cols = log.select_dtypes(include="number").columns
    if len(numeric_cols) == 0:
        st.info("Keine numerischen Spalten - Numeric Outliers übersprungen.")
        return

    selected_numeric = st.selectbox(
        "Numerische Spalte wählen:",
        numeric_cols
    )

    st.write("### Quantile Einstellungen für Numeric")
    lower_num = st.slider("Unteres Quantil (Numeric)", 0.0, 0.5, 0.10, 0.01)
    upper_num = st.slider("Oberes Quantil (Numeric)", 0.5, 1.0, 0.90, 0.01)
    factor_num = st.slider("IOR-Faktor (Numeric)", 1.0, 5.0, 1.5, 0.1)

    outliers_numeric, bounds_numeric = outlier_numeric.numeric_outliers(
        log, selected_numeric, lowerq=lower_num, upperq =upper_num, factor=factor_num
    )
    st.write(f"Schwellenwerte: {bounds_numeric}")
    st.dataframe(outliers_numeric, use_container_width=True)

