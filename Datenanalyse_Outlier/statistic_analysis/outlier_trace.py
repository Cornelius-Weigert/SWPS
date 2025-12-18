import pandas as pd
import streamlit as st
from . import duration_process

if 'lower_case' not in st.session_state:
    st.session_state['lower_case'] = 0.05

if 'upper_case' not in st.session_state:
    st.session_state['upper_case'] = 0.95

if 'factor_case' not in st.session_state:
    st.session_state['factor_case'] = 1.5

def outlier_trace(log_df, case_col="case_id"):
    """
    Detect outliers in traces based on various criteria.
    Args:
        log (pd.DataFrame): DataFrame containing the event log.
        case_col (str): Column name for case IDs.
    Returns:
        dict: Dictionary containing lists of outlier trace indices for each criterion.
    """
    #+++++++Wenn der Trace ungewöhnlich lang ist+++++++++++++
    outliers = {}
    st.subheader("❗️ Filter - Case Duration")

    case_duration = duration_process.duration_pro_case(log_df)
    #if case_duration is not None and not case_duration.empty:
    show_case_slider = st.checkbox("Perzentilebasierte Grenzwerte anzeigen ", value = False,key="case_slider")
    if show_case_slider:
        st.write("Perzentilebasierte Grenzenwerte(Case Duration)")
        lower_case = st.slider("Untere Grenze (Case)", 0.0, 0.5, 0.10, 0.01,help="Der Anzahl von Case-Dauer, der die Dauern so teilt, dass x% der Dauern kürzer oder gleich diesem Wert treiben(und y% länger)")
        upper_case = st.slider("Obere Grenze (Case)", 0.5, 1.0, 0.90, 0.01,help="Der Anzahl von Case-Dauer, der die Dauern so teilt, dass y% der Dauern kürzer oder gleich diesem Wert treiben(und x% länger)")
        factor_case = st.slider("Faktor (Case)", 1.0, 5.0, 1.5, 0.1,help="Ein häufig verwendeter Faktor (meist 1,5), um Ausreißer zu identifizieren")
        st.session_state['lower_case'] = lower_case
        st.session_state['upper_case'] = upper_case
        st.session_state['factor_case'] = factor_case
     
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