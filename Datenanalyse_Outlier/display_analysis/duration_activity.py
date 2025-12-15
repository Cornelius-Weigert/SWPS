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

    # Dauer pro Aktivität anzeigen
    act = duration_pro_activity(log_df)
    # if act is not None:
    #     st.dataframe(act)
   
    #Avg. Min & Max pro Aktivität anzeigen
    act_summary = act.groupby("activity")["Activity_Duration"].agg(['mean', 'min', 'max']).reset_index()
    st.subheader("📈 Zusammenfassung pro Aktivität")
    st.dataframe(act_summary)

    st.subheader("🕒 Dauer pro Aktivität")
    st.write("---")
    # Display summary statistics for each activity
    for _, row in act_summary.iterrows():
        st.write(f"**Aktivität:** {row['activity']}")
        st.write(f"Durchschnittliche Dauer: {row['mean']}")
        st.write(f"Kürzeste Dauer: {row['min']}")
        st.write(f"Längste Dauer: {row['max']}")

        st.write("---")
