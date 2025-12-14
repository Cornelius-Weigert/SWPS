import streamlit as st

def show_resources(log_df, resource_col="resource"):
    """
    Show resource analysis in the Streamlit interface.
    Args:
        log_df (pd.DataFrame): The event log as a DataFrame.
        resource_col (str): The name of the resource column in the DataFrame.
    Returns:
        None
    """
    st.subheader("👥 Ressourcen Analyse")

    if resource_col not in log_df.columns:
        st.info("Keine Ressourcenspalte gefunden.")
        return
    
    activities = log_df["activity"].unique()
    selected = st.selectbox("Aktivität wählen", activities)

    sub = log_df[log_df["activity"] == selected]
    counts = sub["resource"].value_counts()

    st.bar_chart(counts, sort=False) # sort=False to keep the original pre sorted order -> otherwise it sorts alphabetically

    log_with_counts = log_df.groupby("resource").agg(activity_count=("activity", "count")).reset_index()

    st.subheader("📊 Ereignisse pro Ressource")

    st.bar_chart(log_with_counts, x="resource", y="activity_count")       