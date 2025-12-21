import streamlit as st
from ..statistic_analysis.outlier_trace import outlier_trace
from ..statistic_analysis.duration_process import duration_pro_case
from .outlier_acception import accept_outliers
from ..statistic_analysis.second_to_time import second_to_time
from ..statistic_analysis.duration_activity import duration_pro_activity
from ..statistic_analysis import duration_process

def show_trace_outliers(log_df):
    """
    Show trace outlier analysis in the Streamlit interface.
    Args:
        log_df (pd.DataFrame): The event log as a DataFrame.
    Returns:    
        None
    """
    #filter
    st.subheader("🌟 Filter - Case Duration")
    case_duration = duration_process.duration_pro_case(log_df)
    show_case_slider = st.checkbox("Perzentilebasierte Grenzwerte anzeigen ", value = False,key="case_slider")
    lower_case=st.session_state['lower_case'] = 0.05
    upper_case=st.session_state['upper_case'] = 0.95
    factor_case=st.session_state['factor_case'] = 1.5
    if show_case_slider:
            st.write("Perzentilebasierte Grenzenwerte(Case Duration)")
            lower_case = st.slider("Untere Grenze (Case)", 0.0, 0.5, lower_case, 0.01,help="Der Anzahl von Case-Dauer, der die Dauern so teilt, dass x% der Dauern kürzer oder gleich diesem Wert treiben(und y% länger)")
            upper_case = st.slider("Obere Grenze (Case)", 0.5, 1.0,upper_case, 0.01,help="Der Anzahl von Case-Dauer, der die Dauern so teilt, dass y% der Dauern kürzer oder gleich diesem Wert treiben(und x% länger)")
            factor_case = st.slider("Faktor (Case)", 1.0, 5.0, factor_case, 0.1,help="Ein häufig verwendeter Faktor (meist 1,5), um Ausreißer zu identifizieren")
            st.session_state['lower_case'] = lower_case
            st.session_state['upper_case'] = upper_case
            st.session_state['factor_case'] = factor_case


    outliers = outlier_trace(log_df)
    case_duration_df = duration_pro_case(log_df)
    # activity duration
    activity_df = duration_pro_activity(log_df)

    for category, indices in outliers.items():
        with st.expander(f"### Kategorie: {category} | Anzahl Cases: {len(set(log_df.loc[indices, 'case_id']))}"):
            if indices:
                outlier_df = log_df.loc[indices]
            else:
                st.write("Keine Ausreißer in dieser Kategorie gefunden.")
                continue
            
            outlier_df=outlier_df.merge(
                    case_duration_df[["case_id","case_duration"]]  ,
                    on=["case_id"],
                    how="left"
                )
            outlier_df=outlier_df.merge(
                activity_df[
                        ["case_id", "timestamp","Activity_Duration_time"]
                    ],
                    on=["case_id","timestamp"],
                    how="left"   
            )

            # mit expander nach case gruppieren und anzeige 
            for case_id, case_df in outlier_df.groupby("case_id"):
                case_duration=second_to_time(case_df["case_duration"].iloc[0])
                with st.expander(f"Trance von Case ID: {case_id}  |   Case_Dauer:{case_duration}"):
                    st.dataframe(case_df[
                            ["activity","resource","timestamp","Activity_Duration_time"]]
                        , width="stretch",hide_index=True)
                
