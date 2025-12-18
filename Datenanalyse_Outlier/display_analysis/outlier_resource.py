import streamlit as st
from ..statistic_analysis.outlier_resource import outlier_resources

def show_resource_outliers(log_df):
    """
    Show resource outlier analysis in the Streamlit interface.
    Args: 
        log_df (pd.DataFrame): The event log as a DataFrame.
    Returns:
        None
    """

    st.subheader("❗️ Ausreißer - Ressourcen")

    display_cols=["case_id","activity","resource","timestamp","resource_activity_count"]

    outliers,log_with_counts = outlier_resources(log_df)

    resource_activity_count = (log_df.groupby("resource").size().reset_index(name="resource_activity_count"))


    for category, indices in outliers.items():
        st.write(f"### Kategorie: {category}")
        if indices:
            outlier_df = log_df.loc[indices]
            outlier_df = outlier_df.merge(
            resource_activity_count,
            on="resource",
            how="left"
            )
            st.dataframe(outlier_df[display_cols], width="stretch",hide_index=True)
        else:
            st.write("Keine Ausreißer in dieser Kategorie gefunden.")