import streamlit as st
from statistic_analysis.standard_compare import compare_with_standardwert
from statistic_analysis.time_analysis import time_analysis1
from statistic_analysis.duration import duration_pro_activity

def show_standard_compare(log, standard_dict=None,source_col="value"):
    if log is None:
        st.warning("kein Eventlog geladen")
        return
    

    #Case Duration
    durations=time_analysis1(log)
    if durations is not None:
        standard_duration=durations["Dauer"].mean()
        df_standard= compare_with_standardwert(durations, standard_duration, value_col="Dauer")
        st.subheader("📊Case Duration: Standardwerte & Abweichungen")
        st.dataframe(df_standard)
     #st.dataframe(durations)
    

    # Activity Duration
    activity_durations=duration_pro_activity(log)
    if activity_durations is not None:
        standard_activity = activity_durations["Activity_Duration"].mean()
        df_activity_standard = compare_with_standardwert(activity_durations, standard_activity, value_col="Activity_Duration")
        st.subheader("📊Activity Duration: Standardwerte & Abweichung")
        st.dataframe(df_activity_standard)





    
        #  value
    numeric_cols = log.select_dtypes(include="number").columns
    for col in numeric_cols:
        standard_value = log[col].mean()
        df_std = compare_with_standardwert(log, standard_value, value_col=col)
        st.subheader(f"📊Value: Standardwerte & Abweichung")
        st.dataframe(df_std)
