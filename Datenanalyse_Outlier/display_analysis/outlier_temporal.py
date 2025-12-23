import streamlit as st
from ..statistic_analysis.outlier_temporal import temporal_outliers
import pandas as pd
from ..statistic_analysis.second_to_time import second_to_time
from .outlier_acception import accept_outliers
from ..statistic_analysis import duration_activity
from .description import OUTLIER_DESCRIPTIONS

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
    #filter 
    st.subheader("🌟 Filter - Activity Duration")
    show_act_slider = st.checkbox("Perzentilebasierte Grenzwerte anzeigen ", value = False,key="actvity_slider")
    lower_act =st.session_state['lower_act']
    upper_act=st.session_state['upper_act']
    factor_act=st.session_state['factor_act']
    if show_act_slider: 
        st.write("Perzentilbasierte Grenzwerte (Activity Duration)")
        lower_act = st.slider("Untere Grenze(Activity)", 0.0, 0.5, lower_act, 0.01,help="Der Anzahl von Aktivität-Dauer, der die Dauern so teilt, dass x% der Dauern kürzer oder gleich diesem Wert treiben(und y% länger)")
        upper_act = st.slider("Obere Grenze (Activity)", 0.5, 1.0, upper_act, 0.01,help="Der Anzahl von Aktivität-Dauer, der die Dauern so teilt, dass y% der Dauern kürzer oder gleich diesem Wert treiben(und x% länger)")
        factor_act = st.slider("Faktor (Activity)", 1.0, 5.0, factor_act, 0.1,help="Ein häufig verwendeter Faktor (meist 1,5), um Ausreißer zu identifizieren")
        st.session_state['lower_act'] = lower_act
        st.session_state['upper_act'] = upper_act
        st.session_state['factor_act'] = factor_act


    outliers, log_with_duration = temporal_outliers(log_df, case_col=case_col)

    # duration auch anzeigen
    for category, indices in outliers.items():
        st.write(f"### Kategorie: {category}")
        if category in OUTLIER_DESCRIPTIONS:
            st.caption(OUTLIER_DESCRIPTIONS[category]["description"])

        if indices:
            outlier_df = log_with_duration.loc[indices].copy()

            
            if "duration" not in outlier_df.columns:
                outlier_df["duration"] = pd.NA

            # duration nach timestamp_col sortieren
            cols = list(outlier_df.columns)
            if timestamp_col in cols:
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

            # ojektiv -> numeric  ->lesbare Zeit
            if pd.api.types.is_timedelta64_dtype(outlier_df["duration"]):
                outlier_df["duration"] = outlier_df["duration"].dt.total_seconds()
            else:
                outlier_df["duration"] = pd.to_numeric(outlier_df["duration"], errors='coerce')
            outlier_df["duration"] = outlier_df["duration"].apply(second_to_time)

            outlier_df["standard_activity_duration"]= outlier_df["standard_activity_duration"].apply(second_to_time)
            
            # display in dataframe with selectable rows
            outliers = st.dataframe(
                outlier_df, 
                width="stretch",
                on_select="rerun",
                selection_mode="multi-row",
                hide_index=True,
                key=f"df_temporal_outliers_{category}")
            comment = st.text_input("(optional) Kommentar zu ausgewählten Ausreißern eingeben",key=f"comment_temporal_{category}")
            ausreißer_akzeptiert_button = st.button("Ausgewählte Ausreißer akzeptieren", key=f"accept_temporal_{category}")
            if ausreißer_akzeptiert_button:
                accept_outliers(outliers.selection.rows,category,outlier_df,comment,"temporal")
        else:
            st.write("Keine Ausreißer in dieser Kategorie gefunden.")