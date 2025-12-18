import streamlit as st
from ..statistic_analysis.outlier_trace import outlier_trace
from ..statistic_analysis.duration_process import duration_pro_case
from ..statistic_analysis.second_to_time import second_to_time
from ..statistic_analysis.duration_activity import duration_pro_activity

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
    # activity duration
    activity_df = duration_pro_activity(log_df)


    for category, indices in outliers.items():
        st.write(f"### Kategorie: {category}")
        if indices:
            outlier_df = log_df.loc[indices]
        else:
            st.write("Keine Ausreißer in dieser Kategorie gefunden.")
        
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
        
        for case_id, case_df in outlier_df.groupby("case_id"):
            case_duration=second_to_time(case_df["case_duration"].iloc[0])
   
    

        # mit expander nach case gruppieren und anzeige 
        for case_id, case_df in outlier_df.groupby("case_id"):
            with st.expander(f"Trance von Case ID: {case_id}  |   Case_Dauer:{case_duration}"):
                st.dataframe(case_df[
                        ["activity","resource","timestamp","Activity_Duration_time"]]
                       , width="stretch",hide_index=True)
                