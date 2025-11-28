import streamlit as st
from statistic_analysis import numeric

def show_numeric(log):
    st.subheader("🔢 Numerische Analyse")
    stats = numeric.numeric1(log)
    if stats is not None:
        st.dataframe(stats)
    else:
        st.info("Keine numerischen Spalten gefunden.")
