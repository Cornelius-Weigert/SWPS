import streamlit as st
from ..statistic_analysis import duration_process
from ..statistic_analysis import duration_activity

def show_process_duration(log):
    st.subheader("⏰ Prozessdauer")
    durations = duration_process.duration_pro_case(log)
    if durations is not None:
        # st.dataframe(durations, use_container_width=True)
        st.write("Durchschnittliche Prozessdauer:",durations["Dauer"].mean())
        st.write("Kürzeste Prozessdauer:", durations["Dauer"].min())
        st.write("Längste Prozessdauer", durations["Dauer"].max())
    
 


