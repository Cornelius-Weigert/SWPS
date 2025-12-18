import pandas as pd
from .second_to_time import second_to_time
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
    case_duration["case_duration"]=(case_duration["last"]- case_duration["first"])
    #in Sekunde
    case_duration["case_duration"] = (case_duration["last"] - case_duration["first"]).dt.total_seconds()

    case_duration = case_duration.reset_index()
    case_duration["case_duration_time"]=(case_duration["case_duration"].apply(second_to_time))


    return case_duration[[case_col, "case_duration","case_duration_time"]]