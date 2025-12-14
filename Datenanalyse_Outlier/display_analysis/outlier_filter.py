import streamlit as st
from ..statistic_analysis import (
    duration_activity,
    duration_process
)

def adapt_outlier_filter(log_df):
    """
    Show outlier filters & let user adapt them in the Streamlit interface.
    Args:
        log_df (pd.DataFrame): The event log as a DataFrame.
    Returns:
        None
    """
    st.subheader("❗️ Filter - Case Duration")

    case_duration = duration_process.duration_pro_case(log_df)
    if case_duration is not None:
        st.write("### Quantile Einstellungen für Case Duration")
        lower_case = st.slider("Unteres Quantil (Case)", 0.0, 0.5, 0.10, 0.01)
        upper_case = st.slider("Oberes Quantil (Case)", 0.5, 1.0, 0.90, 0.01)
        factor_case = st.slider("IQR-Faktor (Case)", 1.0, 5.0, 1.5, 0.1)
        st.session_state['lower_case'] = lower_case
        st.session_state['upper_case'] = upper_case
        st.session_state['factor_case'] = factor_case

    else:
        st.info("Keine Zeitdaten - Case Duration Outliers übersprungen.")

    st.subheader("❗️ Filter - Activity Duration")

    activity_df = duration_activity.duration_pro_activity(log_df)
    if activity_df is not None:
        st.write("### Quantile Einstellungen für Activity Duration")
        lower_act = st.slider("Unteres Quantil (Activity)", 0.0, 0.5, 0.10, 0.01)
        upper_act = st.slider("Oberes Quantil (Activity)", 0.5, 1.0, 0.90, 0.01)
        factor_act = st.slider("IQR-Faktor (Activity)", 1.0, 5.0, 1.5, 0.1)
        st.session_state['lower_act'] = lower_act
        st.session_state['upper_act'] = upper_act
        st.session_state['factor_act'] = factor_act

    else:
        st.info("Keine Aktivitätsdauer - Activity Outliers übersprungen.")