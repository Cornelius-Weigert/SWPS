def frequency1(log_df, event_col="activity"):
    """
    Calculate the frequency of each event in the log.
    Args:
        log_df (pd.DataFrame): DataFrame containing the event log.
        event_col (str): Column name for events.
    Returns:
        pd.DataFrame: DataFrame with event frequencies.
    """
    freq = log_df[event_col].value_counts().reset_index()
    freq.columns = ["Event", "Häufigkeit"]
    return freq

def frequency_unique(log_df, event_col="activity", case_col="case_id"):
    """
    Calculate the frequency of each unique event in the log
    """
    unique_freq = log_df.groupby(event_col)[case_col].nunique().reset_index()
    unique_freq.columns = ["Event", "Unique_Häufigkeit"]
    return unique_freq

