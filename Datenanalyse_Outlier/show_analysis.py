import streamlit as st
import pandas as pd
import pm4py

from Datenanalyse_Outlier.statistic_analysis.duration_activity import duration_pro_activity
from Datenanalyse_Outlier.statistic_analysis.duration_process import duration_pro_case
from Datenanalyse_Outlier.statistic_analysis.frequency import frequency1
from Datenanalyse_Outlier.statistic_analysis.outlier_activity_duration import activity_duration_outliers
from Datenanalyse_Outlier.statistic_analysis.outlier_case_duration import case_duration_outliers
from Datenanalyse_Outlier.statistic_analysis.outlier_resource import outlier_resources
from Datenanalyse_Outlier.statistic_analysis.outlier_temporal import temporal_outliers
from Datenanalyse_Outlier.statistic_analysis.outlier_trace import outlier_trace
from Datenanalyse_Outlier.statistic_analysis.standard_compare import compare_with_standardwert
from Datenanalyse_Outlier.map_columns import map_column

def show_all_analysis(log_df):

    # Absicherung, falls kein Dataframe übergeben
    if not isinstance(log_df, pd.DataFrame):
        log_df = pm4py.convert_to_dataframe(log_df)
        
    log_df = map_column(log_df)

    # Feature-Berechnung 
    duration_activity = duration_pro_activity(log_df)
    duration_process = duration_pro_case(log_df)

    # Outlier-Berechnung auf Features
    activity_duration = activity_duration_outliers(duration_activity)
    case_duration = case_duration_outliers(duration_process)

    # Direkt-Analysen
    frequency = frequency1(log_df)
    temporal = temporal_outliers(log_df)
    resource = outlier_resources(log_df)
    trace = outlier_trace(log_df)
    standard_compare = compare_with_standardwert(log_df)

    #duration_activity = duration_pro_activity(log_df)
    #duration_process = duration_pro_case(log_df)
    #frequency = frequency1(log_df)
    #activity_duration = activity_duration_outliers(log_df)
    #case_duration = case_duration_outliers(log_df)
    #temporal = temporal_outliers(log_df)
    #resource = outlier_resources(log_df)
    #trace = outlier_trace(log_df)
    #standard_compare = compare_with_standardwert(log_df)
    
    # Anzeigen
    #st.dataframe(duration_activity)
    #st.dataframe(duration_process)
    #st.dataframe(frequency)
    #st.dataframe(activity_duration)
    #st.dataframe(case_duration)
    #st.dataframe(temporal)
    #st.dataframe(resource)
    #st.dataframe(trace)
    #st.dataframe(standard_compare)

    # Ergebnisse zurückgeben
    return {
        "duration_activity": duration_activity,
        "duration_process": duration_process,
        "frequency": frequency,
        "activity_duration": activity_duration,
        "case_duration": case_duration,
        "temporal": temporal,
        "resource": resource,
        "trace": trace,
        "standard_compare": standard_compare, 
    }
