import streamlit as st
from statistic_analysis import time_analysis
from statistic_analysis import duration

def show_duration(log):
    st.subheader("⏰ Prozessdauer")
    durations = time_analysis.time_analysis1(log)
    if durations is not None:
        st.dataframe(durations)


    st.subheader("🕒 Dauer pro Aktivität")
    act = duration.duration_pro_activity(log)
    if act is not None:
        st.dataframe(act)
