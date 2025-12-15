import streamlit as st
from .outlier_filter import adapt_outlier_filter

 

def show_all_analysis(log_df):
    """
    show_all_analysis zeigt alls statistischen Analysen des Eventlogs in Streamlit an.
    
    :param log: das Eventlog als dataframe

    :tabs  
        Ausreißer_Temporal,
        Ausreißer_Ressourcen,
        Ausreißer_Trace,  
        Standardwerte-Vergleich,
        Filter,
        Häufigkeit,
    
        Prozessdauer,
        Zeit-Analyse,
        Ressourcen,
    """
  
    tab4 = st.tabs([
        "Ausreißer-Filter",
    ])
    
    with tab4:
        adapt_outlier_filter(log_df)