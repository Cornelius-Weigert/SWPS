import streamlit as st
from ..statistic_analysis import frequency

def show_frequency(log_df, case_col="case_id", event_col="activity"):
    """
    Show frequency analysis in the Streamlit interface.
    Args:   
         log_df (pd.DataFrame): The event log as a DataFrame.
     Returns:
         None
    """
    st.subheader("📌 Häufigkeit Analyse")

    freq_total = frequency.frequency1(log_df, event_col)
    freq_unique = frequency.frequency_unique(log_df, event_col, case_col)

    # merge total & unique
    freq_df = freq_total.merge(freq_unique, on="Event")

    st.write("Häufigkeit pro Event/unique Event:")
    st.dataframe(freq_df)

    st.bar_chart(freq_df, x="Event", y="Häufigkeit")
    st.bar_chart(freq_df, x="Event", y="Unique_Häufigkeit")

   