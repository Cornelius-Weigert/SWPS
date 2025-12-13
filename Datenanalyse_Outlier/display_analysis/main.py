import streamlit as st
from .frequency import show_frequency
from .duration_process import show_process_duration
from .outlier_filter import show_outliers
from .resources import show_resources
from .duration_activity import show_activity_duration
from .standard_value import show_standard_compare
import pandas as pd
from .duration_process import show_process_duration
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
  
  ############################
    #if'timestamp' in log.columns:
    #    log['timestamp'] = pd.to_datetime(log['timestamp'], errors='coerce')

    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9= st.tabs([
        "Ausreißer-Temporal", 
        "Ausreißer-Trace",
        "Ausreißer-Ressourcen",
        "Ausreißer-Filter",
        "Standardwerte-Vergleich",
        "Häufigkeit",
        "Prozessdauer",
        "Aktivitätsdauer",
         "Ressourcen", 
    ])

    with tab1:
        show_temporal_outliers(log)
    
    with tab2:
        show_trace_outliers(log)
    
    with tab3:
        show_resource_outliers(log)
    
    with tab4:
        show_outliers(log)
    
    with tab5:
        show_standard_compare(log)
    
    with tab6:
        show_frequency(log)
    
    with tab7:
        show_process_duration(log)
   

    with tab8:
        show_activity_duration(log)

    with tab9:
        show_resources(log)

