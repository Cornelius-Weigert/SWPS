import pandas as pd
from .second_to_time import second_to_time
def compare_with_standardwert(log_df, standard=None, event_col="activity", value_col="value", id_col="case_id"):
    """
    Compare values in the log with standard values.
    Args:
        log (pd.DataFrame): DataFrame containing the event log.
        standard (dict or numeric): Standard values per event or a single standard value.
        event_col (str): Column name for events.
        value_col (str): Column name for values to compare.
    Returns:
        pd.DataFrame: DataFrame with original values, standard values, and deviations.
    """

    if value_col not in log_df.columns:
        return pd.DataFrame()
    
    if standard is None:
        standard = log_df[value_col].median()

    if isinstance(standard,(int, float, pd.Timedelta)):
        log_df["Standard"]=standard 
    else:
        if event_col is not None:
            log_df["Standard"] = log_df[event_col].map(standard)
       
    log_df["Abweichung"] = log_df[value_col] - log_df["Standard"]
    log_df["Abweichung"] = log_df["Abweichung"].apply(second_to_time)

    cols =[]
    if id_col is not None and id_col in log_df.columns:
        cols.append(id_col)
    if event_col is not None and event_col in log_df.columns:
        cols.append(event_col)
    
    cols+= [value_col, "Abweichung"]
    return log_df[cols]














