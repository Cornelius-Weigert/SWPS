import streamlit as st
from ..statistic_analysis.outlier_temporal import temporal_outliers
import pandas as pd
from ..statistic_analysis.second_to_time import second_to_time

def deduplicate_columns(log_df):
    new_cols = []
    seen = {}
    for col in log_df.columns:
        if col in seen:
            seen[col] += 1
            new_cols.append(f"{col}_{seen[col]}")
        else:
            seen[col] = 0
            new_cols.append(col)
    log_df.columns = new_cols
    return log_df

   

def show_temporal_outliers(log_df: pd.DataFrame, case_col="case_id", timestamp_col="timestamp", activity_col="activity"):
    """
    Show temporal outlier analysis based on activity duration in the Streamlit interface.
    Args:
        log_df (pd.DataFrame): The event log as a DataFrame.
        case_col (str): The name of the case identifier column.
        timestamp_col (str): The name of the timestamp column.
        activity_col (str): The name of the activity column.
    Returns:
        None
    """
    st.subheader("❗️ Ausreißer - Zeitlich")

    log_df = deduplicate_columns(log_df)

    outliers, log_with_duration = temporal_outliers(log_df, case_col=case_col)

    # duration auch anzeigen
    for category, indices in outliers.items():
        st.write(f"### Kategorie: {category}")
        if indices:
            outlier_df = log_with_duration.loc[indices].copy()

            
            if "duration" not in outlier_df.columns:
                outlier_df["duration"] = pd.NA

            # duration nach timestamp_col sortieren
            cols = list(outlier_df.columns)
            if timestamp_col in cols:
                #
                cols.remove("duration") if "duration" in cols else None
               
                new_cols = []
                for c in cols:
                    new_cols.append(c)
                    if c == timestamp_col:
                        new_cols.append("duration")
                # append any remaining cols not in new_cols
                for c in cols:
                    if c not in new_cols:
                        new_cols.append(c)
                
                # remove duplicates while preserving order
                new_cols = [c for i, c in enumerate(new_cols) if c not in new_cols[:i]]
                if "duration" not in new_cols:
                    new_cols.append("duration")
               

                new_cols = [c for c in new_cols if c in outlier_df.columns]
                outlier_df = outlier_df.reindex(columns=new_cols)
            else:
                # falls kein timestamp_col, duration an den Anfang setzen
                cols = outlier_df.columns.tolist()
                if "duration" in cols:
                    cols.remove("duration")
                    cols.insert(0, "duration")
                    outlier_df = outlier_df.reindex(columns=cols)

            #ojektiv -> numeric  ->lesbare Zeit
            if pd.api.types.is_timedelta64_dtype(outlier_df["duration"]):
                outlier_df["duration"] = outlier_df["duration"].dt.total_seconds()
            else:
                outlier_df["duration"] = pd.to_numeric(outlier_df["duration"], errors='coerce')
            outlier_df["duration"] = outlier_df["duration"].apply(second_to_time)

            outlier_df["standard_activity_duration"]= outlier_df["standard_activity_duration"].apply(second_to_time)
            

            # display in dataframe with selectable rows
            st.dataframe(
                outlier_df, 
                width="stretch",
                on_select="rerun",
                selection_mode="multi-row",
                hide_index=True,)
        else:
            st.write("Keine Ausreißer in dieser Kategorie gefunden.")