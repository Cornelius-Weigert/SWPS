import streamlit as st

# --- SESSION STATE INITIALISIEREN ---
st.session_state.setdefault("uploaded_logs", [])
st.session_state.setdefault("latest_upload", None)
st.session_state.setdefault("file_name", None)
st.session_state.setdefault("outlier_total", 0)
st.session_state.setdefault("outlier_checked", 0)

st.set_page_config(page_title="Dashboard", layout="wide")

# --- Dashboard Header ---
st.title("🏠 Dashboard")
st.write("Willkommen zur Übersicht deiner Process-Mining-App!")

# --- METRICS ---
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Hochgeladene Logs", len(st.session_state["uploaded_logs"]))

with col2:
    st.metric(
        "Ausreißer gefunden",
        st.session_state["outlier_total"],
        f"{st.session_state['outlier_checked']} geprüft"
    )

with col3:
    st.metric("Letzter Upload", st.session_state["latest_upload"] or "Keine Uploads")

st.markdown("---")

# --- Neueste Aktivitäten ---
st.subheader("📝 Neueste Aktivitäten")

if st.session_state["uploaded_logs"]:
    for log in reversed(st.session_state["uploaded_logs"][-5:]):
        st.write(f"- 📂 {log}")
else:
    st.write("Keine Aktivitäten bisher.")


