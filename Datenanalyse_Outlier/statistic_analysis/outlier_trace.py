import pandas as pd
import streamlit as st
from . import duration_process

def outlier_trace(log_df, case_col="case_id"):
    """
    Detect outliers in traces based on various criteria.
    Args:
        log (pd.DataFrame): DataFrame containing the event log.
        case_col (str): Column name for case IDs.
    Returns:
        dict: Dictionary containing lists of outlier trace indices for each criterion.
    """
    outliers = {}
    #+++++++Wenn der Trace ungewöhnlich lang ist+++++++++++++
    trace_lengths = log_df.groupby(case_col).size()
    length_threshold = trace_lengths.quantile(st.session_state['upper_case']) 
    long_trace_cases = trace_lengths[trace_lengths > length_threshold].index
    long_trace_rows = log_df[log_df[case_col].isin(long_trace_cases)]
    outliers['long-traces'] = long_trace_rows.index.tolist()

    #+++++++Wenn der Trace ungewöhnlich kurz ist+++++++++++++
    short_trace_cases = trace_lengths[trace_lengths < trace_lengths.quantile(st.session_state['lower_case'])].index
    short_trace_rows = log_df[log_df[case_col].isin(short_trace_cases)]
    outliers['short-traces'] = short_trace_rows.index.tolist()      

    #+++++++Trace Varianten herausfiltern+++++++++++++
    trace_variants = log_df.groupby(case_col).apply(lambda x: tuple(x['activity'].tolist()))

    #+++++++Wenn der Trace zu viele verschiedene Aktivitäten hat+++++++++++++
    trace_activity_counts = log_df.groupby(case_col)['activity'].nunique()
    diverse_activity_cases = trace_activity_counts[trace_activity_counts > trace_activity_counts.quantile(0.95)].index
    diverse_activity_rows = log_df[log_df[case_col].isin(diverse_activity_cases)]
    outliers['many-activity-traces'] = diverse_activity_rows.index.tolist()  
   

    #+++++++Wenn der Trace zu wenige verschiedene Aktivitäten hat+++++++++++++
    uniform_activity_cases = trace_activity_counts[trace_activity_counts < trace_activity_counts.quantile(0.05)].index
    uniform_activity_rows = log_df[log_df[case_col].isin(uniform_activity_cases)]
    outliers['uniform-activity-traces'] = uniform_activity_rows.index.tolist()  

    #+++++++Wenn der Trace ungewöhnliche Aktivitäten-Sequenzen hat+++++++++++++
   
    # Trace, die nur einmal vorkommen
    sequence_counts = trace_variants.value_counts()
    unusual_sequences = sequence_counts[sequence_counts == 1].index
    unusual_sequence_cases = trace_variants[trace_variants.isin(unusual_sequences)].index
    unusual_sequence_rows = log_df[log_df[case_col].isin(unusual_sequence_cases)] 
    outliers['unusual-sequence-traces'] = unusual_sequence_rows.index.tolist()  

    #+++++++Wenn der Trace fehlende Aktivitäten hat+++++++++++++
    # weniger als 2
    missing_activity_cases = trace_activity_counts[trace_activity_counts < 2].index
    missing_activity_rows = log_df[log_df[case_col].isin(missing_activity_cases)]
    outliers['missing-activity-traces'] = missing_activity_rows.index.tolist()

    return outliers