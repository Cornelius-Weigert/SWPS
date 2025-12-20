from .second_to_time import second_to_time
def duration_pro_activity(log_df, case_col="case_id", event_col="activity", time_col="timestamp"):
    """
    Calculate the duration of each activity in the log.
     Args:
        log (pd.DataFrame): DataFrame containing the event log.
        case_col (str): Column name for case IDs.
        event_col (str): Column name for activities.
        time_col (str): Column name for timestamps.
     Returns:
        pd.DataFrame: DataFrame with activity durations and standard durations.
    """

    activity_df = log_df.sort_values(by=[case_col, time_col]).copy()

    #next timestamp
    activity_df["next_time"] = activity_df.groupby(case_col)[time_col].shift(-1)
    #duration 
    activity_df["Activity_Duration"] = activity_df["next_time"] - activity_df[time_col]
    #->in Sekunde
    activity_df["Activity_Duration"] = activity_df["Activity_Duration"].dt.total_seconds()
    #->lesbare Zeit
    activity_df["Activity_Duration_time"] = activity_df["Activity_Duration"].apply(second_to_time)

    #standard duration pro Aktivität(durchschnitt)
    standard_activity_duration = activity_df.groupby(event_col)["Activity_Duration"].mean().reset_index()
    standard_activity_duration.columns = [event_col, "standard_activity_duration"]
    activity_df = activity_df.merge(
        standard_activity_duration,
        on=event_col,
        how="left"
    )


    return activity_df