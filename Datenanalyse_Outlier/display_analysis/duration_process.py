import streamlit as st
from ..statistic_analysis import duration_process
from ..statistic_analysis.second_to_time import second_to_time

def show_process_duration(log_df):
    """
    Show process duration analysis in the Streamlit interface.
    Args:
        log_df (pd.DataFrame): The event log as a DataFrame.
    Returns:
        None
    """
    st.subheader("⏰ Prozessdauer")
    case_duration = duration_process.duration_pro_case(log_df)
    if case_duration is not None:
        avg_case=case_duration["case_duration"].mean()
        st.write("Durchschnittliche Prozessdauer:",second_to_time(avg_case))
        min_case=case_duration["case_duration"].min()
        st.write("Kürzeste Prozessdauer:", second_to_time(min_case))
        max_case=case_duration["case_duration"].max()
        st.write("Längste Prozessdauer:", second_to_time(max_case))