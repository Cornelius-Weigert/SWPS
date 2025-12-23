import streamlit as st


with open("Dashboard_log/d_log.txt", "r+") as dashboard_log: # first line safes accepted outliers, second line safes uploaded logs
    lines = dashboard_log.readlines()
    if not lines:
        st.session_state["uploaded_logs"] = []
        st.session_state["outlier_accepted"] = 0
        st.session_state["latest_upload"] = "Keine Uploads"
    else:
        if "outlier_accepted" in st.session_state:
            dashboard_log.seek(0)
            lines[0] = str(st.session_state["outlier_accepted"]) + "\n"
            dashboard_log.writelines(lines)
            dashboard_log.truncate()

        st.session_state["outlier_accepted"] = int(lines[0].strip()) if lines else 0
        st.session_state["uploaded_logs"] = eval(lines[1].strip()) if len(lines) > 1 else []
        st.session_state["latest_upload"] = st.session_state["uploaded_logs"][-1] if st.session_state["uploaded_logs"] else "Keine Uploads"

st.set_page_config(page_title="Dashboard", layout="wide")


# --- Kopfzeile ---
st.title("🏠 Dashboard")
st.write("Übersicht zur interaktiven Detektion von Ausreißern in Eventlogs")

# --- Spalten ---
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Hochgeladene Logs",
         len(st.session_state.get("uploaded_logs", [])))

with col2:
    st.metric(
        "Ausreißer gefunden",
        st.session_state["outlier_accepted"]
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