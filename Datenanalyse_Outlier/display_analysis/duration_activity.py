import streamlit as st
from ..statistic_analysis import duration_process
from ..statistic_analysis.duration_activity import duration_pro_activity

def show_activity_duration(log):
    st.subheader("⌚️Zeit-Analyse")

    

    st.subheader("🕒 Dauer pro Aktivität")
    act = duration_pro_activity(log)
    if act is not None:
        st.dataframe(act)
        



    st.write("->>>Durchschnittliche Aktivitätsdauer:",act["Activity_Duration"].mean())
    st.write("->>>Kürzeste Aktivitätsdauer:", act["Activity_Duration"].min())
    st.write("->>>Längste Aktivitätsdauer", act["Activity_Duration"].max())