import streamlit as st
from ..statistic_analysis.outlier_temporal import temporal_outliers
import pandas as pd


def deduplicate_columns(log):
    new_cols = []
    seen = {}
    for col in log.columns:
        if col in seen:
            seen[col] += 1
            new_cols.append(f"{col}_{seen[col]}")
        else:
            seen[col] = 0
            new_cols.append(col)
    log.columns = new_cols
    return log

   

def show_temporal_outliers(log: pd.DataFrame, case_col="case_id", timestamp_col="timestamp", activity_col="activity"):
    st.subheader("❗️ Ausreißer - Zeitlich")

  
    log = deduplicate_columns(log)

    outliers, log_with_duration = temporal_outliers(log, case_col=case_col, timestamp_col=timestamp_col)

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

            # Runde die Dauer auf 2 Dezimalstellen
            #(in minuten!)

            #ojektiv -> numeric
            outlier_df["duration"] = pd.to_numeric(outlier_df["duration"], errors='coerce')
            
        
            if "duration" in outlier_df.columns:
                outlier_df["duration"] = outlier_df["duration"].round(2)

            st.dataframe(
                outlier_df, 
                use_container_width=True,
                on_select="rerun",
                selection_mode="multi-row",
                hide_index=True,)
        else:
            st.write("Keine Ausreißer in dieser Kategorie gefunden.")
