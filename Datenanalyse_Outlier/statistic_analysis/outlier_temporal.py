import pandas as pd
import streamlit as st
from .second_to_time import second_to_time
 
def temporal_outliers(log_df, case_col="case_id", activity_col="activity", timestamp_col="timestamp"):
    """
    Detect temporal outliers in the event log.
    Args:
        log_df (pd.DataFrame): DataFrame containing the event log.
        case_col (str): Column name for case IDs.
        activity_col (str): Column name for activities.
        timestamp_col (str): Column name for timestamps.
    Returns:
        dict: Dictionary containing lists of outlier indices for each type of temporal outlier.
        pd.DataFrame: DataFrame with additional duration and standard duration columns.
    """
    log_df[timestamp_col] = pd.to_datetime(log_df[timestamp_col], errors='coerce')
    
    #duration rechnen
    log_df = log_df.sort_values(by=[case_col, timestamp_col])
    log_df['prev_timestamp'] = log_df.groupby(case_col)[timestamp_col].shift(1)
    log_df['prev_activity'] = log_df.groupby(case_col)[activity_col].shift(1)
    log_df['next_activity'] = log_df.groupby(case_col)[activity_col].shift(-1)
    log_df['duration'] = (log_df[timestamp_col] - log_df['prev_timestamp']).dt.total_seconds()


    # Durchschnittliche Dauer pro Aktivität berechnen und anzeigen
    log_df['duration'] = pd.to_numeric(log_df['duration'], errors='coerce')
    standard = log_df.groupby(activity_col)['duration'].mean().rename('standard_activity_duration').reset_index()
    # standard.columns = [activity_col, 'standard_activity_duration']
    log_df = log_df.merge(standard, on=activity_col, how='left')
    # log_df['standard_activity_duration']=log_df['standard_activity_duration']

    
    outliers = {}
    
    #+++++Wenn die timestamp in Zukunft liegt++++++++++++++   
    now = pd.Timestamp.now(tz="Europe/Berlin")
    log_df[timestamp_col] = pd.to_datetime(log_df[timestamp_col])
    if log_df[timestamp_col].dt.tz is None:
        log_df[timestamp_col] = log_df[timestamp_col].dt.tz_localize("Europe/Berlin")
    else:
        log_df[timestamp_col] = log_df[timestamp_col].dt.tz_convert("Europe/Berlin")
    future_rows = log_df[log_df[timestamp_col] > now]
    outliers['Zeitstempel_in_Zukunft'] = future_rows.index.tolist()

    
    #+++++++Wenn Timestamp fehlt+++++++++++++++++++++++++
    missing_timestamp_rows = log_df[log_df[timestamp_col].isnull()]
    outliers['Fehlender_Zeitstempel'] = missing_timestamp_rows.index.tolist()  

    #++++++++Wenn die Dauer zwischen Aktivitäten ungewöhnlich lang ist+++++++++++++
    long_duration_threshold = log_df['duration'].quantile(st.session_state['upper_act'])
    long_duration_rows = log_df[log_df['duration'] > long_duration_threshold]
    outliers['Lange_Aktivitätsdauer'] = long_duration_rows.index.tolist()

    #++++++++Wenn die Dauer zwischen Aktivitäten ungewöhnlich kurz ist+++++++++++++
    short_duration_threshold = log_df['duration'].quantile(st.session_state['lower_act'])  
    short_duration_rows = log_df[log_df['duration'] < short_duration_threshold]
    outliers['Kurze_Aktivitätsdauer'] = short_duration_rows.index.tolist() 

    #+++++++Wenn Timestamp vor dem vorherigen Timestamp liegt+++++++++++++
    negative_duration_rows = log_df[log_df['duration'] < 0]
    outliers['Negative_Aktivitätsdauer'] = negative_duration_rows.index.tolist()

    # Nur relevante Spalten für die Anzeige behalten
    display_cols = [case_col, 'prev_activity',activity_col,'next_activity', timestamp_col, 'prev_timestamp','duration','standard_activity_duration']
    log_df = log_df[display_cols]


    return outliers,log_df
