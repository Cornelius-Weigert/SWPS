import streamlit as st
from ..statistic_analysis.standard_compare import compare_with_standardwert
from ..statistic_analysis.duration_process import duration_pro_case 
from ..statistic_analysis.duration_activity import duration_pro_activity
from ..statistic_analysis.second_to_time import second_to_time

def show_standard_compare(log):
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
        df_standard= compare_with_standardwert(durations,standard_duration, value_col="case_duration",id_col="case_id")

        # standard_duration_time=second_to_time(standard_duration)
        df_standard["case_duration"]=df_standard["case_duration"].apply(second_to_time)
        standard_duration_time=second_to_time(standard_duration)
        st.subheader("📊Case Duration: Standardwerte & Abweichungen")
        st.write(f"🌟Standardwert(Durchschnitt) von Case-Dauer:{standard_duration_time}")
        st.dataframe(df_standard)
    #  st.dataframe(durations)
    
    # Activity Duration
    activity_durations=duration_pro_activity(log)
    if activity_durations is not None:
        standard_activity = activity_durations["Activity_Duration"].mean()
        df_activity_standard = compare_with_standardwert(activity_durations, standard_activity, value_col="Activity_Duration",event_col="activity")

        df_activity_standard["Activity_Duration"]=df_activity_standard["Activity_Duration"].apply(second_to_time)
        standard_activity_time=second_to_time(standard_activity)
        st.subheader("📊Activity Duration: Standardwerte & Abweichung")
        st.write(f"🌟Standardwert(Durchschnitt) von Aktivität-Dauer:{standard_activity_time}")
        st.dataframe(df_activity_standard)





