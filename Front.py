import streamlit as st

# --- GLOBAL PAGE CONFIG ---
st.set_page_config(
    page_title="Process Mining App",
    page_icon="🧭",
    layout="wide"
)

# You can place global CSS here if needed
st.markdown("""
<style>
    .big-title { font-size: 38px !important; font-weight: 700; }
    .subtle { color: #666; margin-bottom: 20px; }
</style>
""", unsafe_allow_html=True)

st.markdown("<p class='big-title'>🧭 Process Mining App</p>", unsafe_allow_html=True)
st.markdown("<p class='subtle'>Nutze das Menü links, um zwischen den Funktionen zu wechseln.</p>", unsafe_allow_html=True)

st.info("➡️ Wähle links im Menü eine Seite aus, z.B. *Dashboard*, *Eventlogs* oder *Ausreißer-Erkennung*.")




import streamlit as st

st.set_page_config(layout="wide")

st.title("🏠 Dashboard")
st.write("Willkommen im Übersichts-Dashboard deiner Process-Mining-Anwendung!")

# --- DASHBOARD CARDS ---
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Hochgeladene Logs", "12", "+2 neue")
with col2:
    st.metric("Analysen ausgeführt", "5", "+1 heute")
with col3:
    st.metric("Ausreißer gefunden", "27", "Letzte Analyse: 8")

st.markdown("---")

st.subheader("📈 Systemstatus")
st.success("Alles funktioniert einwandfrei. Server ist erreichbar.")

st.subheader("📝 Neueste Aktivitäten")
st.write("""
- ✔️ Eventlog *orders_01.xes* hochgeladen  
- ✔️ Ausreißeranalyse auf *eventlog_23.csv* ausgeführt  
- ✔️ CSV-Datei in XES umgewandelt
""")

