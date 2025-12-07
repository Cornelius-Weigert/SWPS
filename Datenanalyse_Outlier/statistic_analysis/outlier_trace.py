import pandas as pd


def outlier_trace(log, case_col="case_id"):
    """
    Identifiziert Ausreißer in Traces basierend auf der Häufigkeit und Länge der Traces.
    Parameter:
    log (pd.DataFrame): Das Ereignisprotokoll als DataFrame.


    Rückgabe:
    pd.DataFrame: DataFrame mit den identifizierten Ausreißern in Traces.
    """
    #+++++++Wenn der Trace ungewöhnlich lang ist+++++++++++++
    outliers = {}
    trace_lengths = log.groupby(case_col).size()
    length_threshold = trace_lengths.quantile(0.95)  # 95. Perzentil als Schwellenwert
    long_trace_cases = trace_lengths[trace_lengths > length_threshold].index
    long_trace_rows = log[log[case_col].isin(long_trace_cases)]
    outliers['long-traces'] = long_trace_rows.index.tolist()    

    #+++++++Wenn der Trace ungewöhnlich kurz ist+++++++++++++
    short_trace_cases = trace_lengths[trace_lengths < trace_lengths.quantile(0.05)].index
    short_trace_rows = log[log[case_col].isin(short_trace_cases)]
    outliers['short-traces'] = short_trace_rows.index.tolist()      

    #+++++++Wenn der Trace selten vorkommt+++++++++++++
    trace_variants = log.groupby(case_col).apply(lambda x: tuple(x['activity'].tolist()))
    variant_counts = trace_variants.value_counts()
    rare_variants = variant_counts[variant_counts < variant_counts.quantile(0.05)].index
    rare_trace_cases = trace_variants[trace_variants.isin(rare_variants)].index
    rare_trace_rows = log[log[case_col].isin(rare_trace_cases)]
    outliers['rare-traces'] = rare_trace_rows.index.tolist()    

    #+++++++Wenn der Trace zu viele verschiedene Aktivitäten hat+++++++++++++
    trace_activity_counts = log.groupby(case_col)['activity'].nunique()
    diverse_activity_cases = trace_activity_counts[trace_activity_counts > trace_activity_counts.quantile(0.95)].index
    diverse_activity_rows = log[log[case_col].isin(diverse_activity_cases)]
    outliers['many-activity-traces'] = diverse_activity_rows.index.tolist()  

    #+++++++Wenn der Trace zu wenige verschiedene Aktivitäten hat+++++++++++++
    uniform_activity_cases = trace_activity_counts[trace_activity_counts < trace_activity_counts.quantile(0.05)].index
    uniform_activity_rows = log[log[case_col].isin(uniform_activity_cases)]
    outliers['uniform-activity-traces'] = uniform_activity_rows.index.tolist()  

    #+++++++Wenn der Trace ungewöhnliche Aktivitäten-Sequenzen hat+++++++++++++
   
    # Trace, die nur einmal vorkommen
    sequence_counts = trace_variants.value_counts()
    unusual_sequences = sequence_counts[sequence_counts == 1].index
    unusual_sequence_cases = trace_variants[trace_variants.isin(unusual_sequences)].index
    unusual_sequence_rows = log[log[case_col].isin(unusual_sequence_cases)] 
    outliers['unusual-sequence-traces'] = unusual_sequence_rows.index.tolist()  

    #+++++++Wenn der Trace fehlende Aktivitäten hat+++++++++++++
   # weniger als 2
    missing_activity_cases = trace_activity_counts[trace_activity_counts < 2].index
    missing_activity_rows = log[log[case_col].isin(missing_activity_cases)]
    outliers['missing-activity-traces'] = missing_activity_rows.index.tolist()



    return outliers