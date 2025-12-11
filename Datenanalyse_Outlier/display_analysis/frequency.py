import streamlit as st
from ..statistic_analysis import frequency

def show_frequency(log):
    st.subheader("📌 Häufigkeit Analyse")
    freq = frequency.frequency1(log)
    st.dataframe(freq)
    st.bar_chart(freq, x="Event", y="Häufigkeit")
