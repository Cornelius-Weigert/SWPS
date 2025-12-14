import streamlit as st
from ..statistic_analysis import frequency

def show_frequency(log_df):
    """
    Show frequency analysis in the Streamlit interface.
    Args:   
        log_df (pd.DataFrame): The event log as a DataFrame.
    Returns:
        None
    """
    st.subheader("📌 Häufigkeit Analyse")
    freq = frequency.frequency1(log_df)
    st.bar_chart(freq, x="Event", y="Häufigkeit")
    st.dataframe(freq)