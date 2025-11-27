import streamlit as st
import os
import tempfile


# --- Upload Funktion ---
def upload_eventlog():
    uploaded_file = st.file_uploader(
        "Datei auswählen", 
        type=["xes", "csv"], 
        key="eventlog_uploader"
    )

    if uploaded_file is not None:

        # Temporäre Datei sichern
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp_file:
            tmp_file.write(uploaded_file.read())
            file_path = tmp_file.name

        extension = os.path.splitext(uploaded_file.name)[1].lower()
        file_type = "XES" if extension == ".xes" else "CSV"

        # Speichern in Session-State
        st.session_state["file_path"] = file_path
        st.session_state["file_type"] = file_type
        st.session_state["file_name"] = uploaded_file.name

        st.success(f"Datei erfolgreich hochgeladen: {uploaded_file.name} ({file_type})")


# --- UI ---
st.title("Eventlog hochladen")

st.write("Bitte Eventlog hochladen (XES oder CSV):")

# Upload immer anzeigen (damit neue Datei geladen werden kann)
upload_eventlog()

# Wenn bereits eine Datei existiert 
if "file_path" in st.session_state:

    st.subheader("Aktuell geladener Eventlog")

    st.write(f"**Dateiname:** {st.session_state['file_name']}")
    st.write(f"**Dateityp:** {st.session_state['file_type']}")
    st.write("**Dateipfad:**")
    st.code(st.session_state["file_path"])
    st.success("Datei gespeichert! Wechsel jetzt zur Tabellenansicht")
