import pandas as pd
def duration_pro_case(log_df, case_col="case_id", time_col="timestamp"):
    """
    Calculate the duration of each case in the log.
     Args:
        log (pd.DataFrame): DataFrame containing the event log.
        case_col (str): Column name for case IDs.
        time_col (str): Column name for timestamps.
    Returns:
        pd.DataFrame: DataFrame with case durations.
    """

    #Sortieren
    df_sorted = log_df.sort_values(by=[case_col, time_col])

    #Durchlaufzeit pro Case
    case_duration = df_sorted.groupby(case_col)[time_col].agg(["first", "last"])
    
    case_duration["case_duration"] = (case_duration["last"] - case_duration["first"]).dt.total_seconds() / 60.0  # (Dauer in Minuten)

    case_duration = case_duration.reset_index()

    return case_duration[[case_col, "case_duration"]]