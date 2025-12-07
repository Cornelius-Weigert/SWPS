import streamlit as st
from display_analysis.frequency import show_frequency
from display_analysis.numeric import show_numeric
from display_analysis.duration import show_duration
from display_analysis.outlier_filter import show_outliers
from display_analysis.resources import show_resources
from display_analysis.time import show_time
from display_analysis.standard_value import show_standard_compare
import pandas as pd
from display_analysis.duration import show_duration
from display_analysis. outlier_temporal import show_temporal_outliers
from display_analysis. outlier_structure import show_structure_outliers
from display_analysis. outlier_resource import show_resource_outliers
from display_analysis. outlier_trace import show_trace_outliers
from display_analysis. outlier_datenattribute import show_datenattribute_outliers

def show_all_analysis(log):
    """
    show_all_analysis zeigt alls statistischen Analysen des Eventlogs in Streamlit an.

    
    :param log: das Eventlog als dataframe

    :tabs  
        Ausreißer_Temporal,
        Ausreißer_Struktur,
        Ausreißer_Ressourcen,
        Ausreißer_Trace,
        Ausreißer_Datenattribute,   
        Standardwerte-Vergleich,
        Filter,
        Häufigkeit,
        
        Numerisch,
        Prozessdauer,
       
        Ressourcen,
        Zeit-Analyse,
        
    """

    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9, tan10,tab11,tab12 = st.tabs([
        "Ausreißer-Temporal", 
        "Ausreißer-Struktur",
        "Ausreißer-Ressourcen",
        "Ausreißer-Trace",
        "Ausreißer-Datenattribute",
        "Ausreißer-Filter",
        "Standardwerte-Vergleich",
    
        "Häufigkeit",
        "Numerisch",
        "Prozessdauer",
        "Ressourcen", 
        "Zeit-Analyse",
        
    ])

    with tab1:
        show_temporal_outliers(log)
    with tab2:
        show_structure_outliers(log)
    with tab3:
        show_resource_outliers(log)
    with tab4:
        show_trace_outliers(log)
    with tab5:
        show_datenattribute_outliers(log)   
    with tab6:
        show_outliers(log)
    with tab7:
        show_standard_compare(log)
    
    with tab8:
        show_frequency(log)

    with tab9:
        show_numeric(log)
    
    with tan10:
        show_duration(log)
    with tab11:
        show_resources(log)

    with tab12:
        show_time(log)


    

