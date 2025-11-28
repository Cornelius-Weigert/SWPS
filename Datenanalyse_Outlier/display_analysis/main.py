import streamlit as st
from display_analysis.frequency import show_frequency
from display_analysis.numeric import show_numeric
from display_analysis.duration import show_duration
from display_analysis.outliers import show_outliers
from display_analysis.resources import show_resources
from display_analysis.time import show_time
from display_analysis.standard_value import show_standard_compare
import pandas as pd
#from statistic_analysis.duration import duration_pro_activity
from statistic_analysis.time_analysis import time_analysis1
from statistic_analysis.standard_compare import compare_with_standardwert
from statistic_analysis.duration import duration_pro_activity

def show_all_analysis(log):
    """
    show_all_analysis zeigt alls statistischen Analysen des Eventlogs in Streamlit an.

    
    :param log: das Eventlog als dataframe

    :tabs  
        Ausreißer,
        Standardwerte-Vergleich,
        Häufigkeit,
        
        Numerisch,
        Prozessdauer,
       
        Ressourcen,
        Zeit-Analyse,
        
    """

    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
        "Ausreißer", 
        "Standardwerte-Vergleich",
        "Häufigkeit",
        "Numerisch",
        "Prozessdauer",
        "Ressourcen", 
        "Zeit-Analyse",
        
    ])

    
    with tab1:
        show_outliers(log)
    with tab2:
        show_standard_compare(log)

    with tab3:
        show_frequency(log)

    with tab4:
        show_numeric(log)

    with tab5:
        show_duration(log)
    with tab6:
        show_resources(log)

    with tab7:
        show_time(log)


    

