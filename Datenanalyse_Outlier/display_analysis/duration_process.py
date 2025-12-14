import streamlit as st
from ..statistic_analysis import duration_process

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
        st.write("Durchschnittliche Prozessdauer:",case_duration["case_duration"].mean())
        st.write("Kürzeste Prozessdauer:", case_duration["case_duration"].min())
        st.write("Längste Prozessdauer", case_duration["case_duration"].max())