import streamlit as st
from statistic_analysis import time_analysis

def show_time(log):
    st.subheader("⌚️Zeit-Analyse")

    durations = time_analysis.time_analysis1(log)
    if durations is None:
        st.info("Keine Timestamps - Analyse übersprungen.")
        return
    

    


    st.dataframe(durations, use_container_width=True)



    st.write("->>>Durchschnittliche Prozessdauer:",durations["Dauer"].mean())
    st.write("->>>Kürzeste Prozessdauer:", durations["Dauer"].min())
    st.write("->>>Längste Prozessdauer", durations["Dauer"].max())




      