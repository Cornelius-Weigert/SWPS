import pandas as pd
import streamlit as st

def outlier_resources(log_df, case_col="case_id", activity_col="activity", resource_col="resource"):
    """
    Detect outliers in resource behavior.
    Args:
        log_df (pd.DataFrame): DataFrame containing the event log.
        case_col (str): Column name for case IDs.
        activity_col (str): Column name for activities.
        resource_col (str): Column name for resources.
    Returns:
        dict: Dictionary containing outlier resource indices for different criteria.
    """
    # Resource-Activity
    counts = log_df.groupby(resource_col)[activity_col].count().reset_index()
    counts.columns = [resource_col, "activity_count"]

    # count auch im log mergen
    log_with_counts = log_df.merge(counts, on=resource_col, how="left")

    outliers = {}

    #+++++++Wenn die Ressource fehlt+++++++++++++++++++++++++
    missing_resource_rows = log_df[log_df[resource_col].isnull()]
    outliers['missing-resource'] = missing_resource_rows.index.tolist() 
    
    #+++++++Wenn eine Ressource ungewöhnlich viele Aktivitäten hat+++++++++++++
    activity_counts = log_df[resource_col].value_counts()

    high_activity_resources = activity_counts[activity_counts > st.session_state['upper_res']].index
    high_activity_rows = log_df[log_df[resource_col].isin(high_activity_resources)]
    outliers['high-activity-resources'] = high_activity_rows.index.tolist()   

    #+++++++Wenn eine Ressource ungewöhnlich wenige Aktivitäten hat+++++++++++++
    low_activity_resources = activity_counts[activity_counts < st.session_state['lower_res']].index
    low_activity_rows = log_df[log_df[resource_col].isin(low_activity_resources)]
    outliers['low-activity-resources'] = low_activity_rows.index.tolist()   

    #+++++++Wenn eine Resource viele verschiedene Aktivitäten ausführt+++++++++++++
    resource_activity_counts = log_df.groupby(resource_col)[activity_col].nunique()
    diverse_activity_resources = resource_activity_counts[resource_activity_counts > resource_activity_counts.quantile(0.95)].index
    diverse_activity_rows = log_df[log_df[resource_col].isin(diverse_activity_resources)]
    outliers['many-activity-resources'] = diverse_activity_rows.index.tolist()   

    return outliers,log_with_counts