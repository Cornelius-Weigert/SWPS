import streamlit as st
from ..statistic_analysis.standard_compare import compare_with_standardwert
from ..statistic_analysis.duration_process import duration_pro_case 
from ..statistic_analysis.duration_activity import duration_pro_activity

def show_standard_compare(log, standard_dict=None,source_col="value"):
    """
    Show standard value comparison analysis in the Streamlit interface.
    Args:
        log (pd.DataFrame): The event log as a DataFrame.
        standard_dict (dict, optional): A dictionary of standard values for comparison.
        source_col (str, optional): The column name to compare with standard values.
    Returns:
        None
    """
    if log is None:
        st.warning("kein Eventlog geladen")
        return
    
    #Case Duration
    durations=duration_pro_case(log)
    if durations is not None:
        standard_duration=durations["case_duration"].mean()
        df_standard= compare_with_standardwert(durations, standard_duration, value_col="case_duration")
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





