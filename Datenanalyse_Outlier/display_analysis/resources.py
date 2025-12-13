import streamlit as st
import matplotlib.pyplot as plt

def show_resources(log):
    st.subheader("👥 Ressourcen Analyse")

    if "org:resource" not in log.columns:
        st.info("Keine Ressourcenspalte gefunden.")
        return
    
    activities = log["concept:name"].unique()
    selected = st.selectbox("Aktivität wählen", activities)

    sub = log[log["concept:name"] == selected]
    counts = sub["org:resource"].value_counts()

    fig = plt.figure()
    counts.plot(kind="bar")
    plt.title(f"Ressourcen für {selected}")
    st.pyplot(fig)



    st.subheader("📊 Ereignisse pro Ressource")

    st.bar_chart(log_with_counts, x="resource", y="activity_count")       
