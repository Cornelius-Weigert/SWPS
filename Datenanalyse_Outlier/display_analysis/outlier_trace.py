import streamlit as st
from ..statistic_analysis.outlier_trace import outlier_trace
from ..statistic_analysis.duration_process import duration_pro_case

def show_trace_outliers(log_df):
    """
    Show trace outlier analysis in the Streamlit interface.
    Args:
        log_df (pd.DataFrame): The event log as a DataFrame.
    Returns:    
        None
    """
    st.subheader("❗️ Ausreißer - Traces")

    outliers = outlier_trace(log_df)
    case_duration_df = duration_pro_case(log_df)

    for category, indices in outliers.items():
        st.write(f"### Kategorie: {category}")
        if indices:
            outlier_df = log_df.loc[indices]
        else:
            st.write("Keine Ausreißer in dieser Kategorie gefunden.")
        
        outlier_df=outlier_df.merge(
                case_duration_df[["case_id","case_duration"]]  ,
                on="case_id",
                how="left"        
            )
        # mit expander nach case gruppieren und anzeige 
        for case_id, case_df in outlier_df.groupby("case_id"):
            with st.expander(f"Trance von Case ID: {case_id}"):
                st.dataframe(case_df[
                    ["activity","resource","timestamp"]
                    + (["case_duration"] if "case_duration" in case_df.columns else []
                       )
            
                ], width="stretch")