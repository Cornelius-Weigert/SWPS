import pandas as pd
import streamlit as st
from .outlier_filter import adapt_outlier_filter
from . outlier_temporal import show_temporal_outliers
from . outlier_resource import show_resource_outliers
from . outlier_trace import show_trace_outliers

 

def show_all_analysis(log):
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
  
    tab1, tab2, tab3, tab4 = st.tabs([
        "Ausreißer-Temporal", 
        "Ausreißer-Trace",
        "Ausreißer-Ressourcen",
        "Ausreißer-Filter",
    ])

    with tab1:
        show_temporal_outliers(log)
    
    with tab2:
        show_trace_outliers(log)
    
    with tab3:
        show_resource_outliers(log)
    
    with tab4:
        adapt_outlier_filter(log)