import streamlit as st
from ..statistic_analysis import (
    duration_activity,
    duration_process,
    outlier_case_duration,
    outlier_activity_duration,
)


def show_outliers(log):

    st.subheader("❗️ Filter - Case Duration")
#
    durations = duration_process.duration_pro_case(log)
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

    activity_df = duration_activity.duration_pro_activity(log)
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


