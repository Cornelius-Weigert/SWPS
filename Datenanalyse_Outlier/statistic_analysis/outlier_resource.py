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
    outliers['Fehlende_Ressource'] = missing_resource_rows.index.tolist() 
    
    #+++++++Wenn eine Ressource ungewöhnlich viele Aktivitäten hat+++++++++++++
    activity_counts = log_df[resource_col].value_counts()

    upper_res=st.session_state.get("upper_res",0.95)
    upper_threshold=activity_counts.quantile(upper_res)

    high_activity_resources = activity_counts[activity_counts > upper_threshold].index
    high_activity_rows = log_df[log_df[resource_col].isin(high_activity_resources)]
    outliers['Ressource_sehr_aktiv'] = high_activity_rows.index.tolist()   

    #+++++++Wenn eine Ressource ungewöhnlich wenige Aktivitäten hat+++++++++++++
    lower_res=st.session_state.get("lower_res",0.05)
    lower_threshold=activity_counts.quantile(lower_res)

    low_activity_resources = activity_counts[activity_counts < lower_threshold].index
    low_activity_rows = log_df[log_df[resource_col].isin(low_activity_resources)]
    outliers['Ressource_wenig_aktiv'] = low_activity_rows.index.tolist()   

    #+++++++Wenn eine Resource viele verschiedene Aktivitäten ausführt+++++++++++++
    resource_unique_activity_counts = log_df.groupby(resource_col)[activity_col].nunique().rename("unique_activity_count")
    # threshold=resource_unique_activity_counts.quantile(0.95)
    upper_res_diverse = st.session_state.get('upper_res_diverse', 0.95)
    threshold = resource_unique_activity_counts.quantile(upper_res_diverse)

    diverse_activity_resources = resource_unique_activity_counts[resource_unique_activity_counts > threshold].index
    diverse_activity_rows = log_df[log_df[resource_col].isin(diverse_activity_resources)]
    outliers['Ressource_vielfältige_Aktivitäten'] = diverse_activity_rows.index.tolist()   

    return outliers,log_with_counts