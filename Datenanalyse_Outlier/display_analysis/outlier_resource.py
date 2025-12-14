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

    display_cols=["case_id","activity","resource","timestamp"]

    outliers, log_with_counts = outlier_resources(log_df)

    for category, indices in outliers.items():
        st.write(f"### Kategorie: {category}")
        if indices:
            outlier_df = log_df.loc[indices, display_cols]
            st.dataframe(outlier_df, width="stretch")
        else:
            st.write("Keine Ausreißer in dieser Kategorie gefunden.")