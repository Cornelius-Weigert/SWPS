import streamlit as st
from ..statistic_analysis.duration_activity import duration_pro_activity

def show_activity_duration(log_df):
    """
    Show activity duration analysis in the Streamlit interface.
    Args:
        log_df (pd.DataFrame): The event log as a DataFrame.
    Returns:
        None
    """
    st.subheader("⌚️Aktivitätsdauer")

    st.subheader("🕒 Dauer pro Aktivität")
    act = duration_pro_activity(log_df)
    if act is not None:
        st.dataframe(act)
    # Summary statistics for all activities
    st.write("Durchschnittliche Aktivitätsdauer:",act["Activity_Duration"].mean())
    st.write("Kürzeste Aktivitätsdauer:", act["Activity_Duration"].min())
    st.write("Längste Aktivitätsdauer", act["Activity_Duration"].max())

    #To Do: Avg. Min & Max pro Aktivität anzeigen