import streamlit as st
import os
import tempfile

# Funktion zum Hochladen 
def upload_eventlog():
    st.write("Bitte Eventlog hochladen (XES oder CSV):")
    
    uploaded_file = st.file_uploader("Datei auswählen", type=["xes", "csv"])
    
    if uploaded_file is not None:
        # Temporäre Datei erstellen, um einen Dateipfad zu haben
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp_file:
            tmp_file.write(uploaded_file.read())
            file_path = tmp_file.name
        
        # Dateityp bestimmen
        extension = os.path.splitext(uploaded_file.name)[1].lower()
        if extension == ".xes":
            file_type = "XES"
        elif extension == ".csv":
            file_type = "CSV"
        else:
            file_type = "Unbekannt"
        
        st.success(f"Datei hochgeladen: {uploaded_file.name} ({file_type})")
        return file_path, file_type
    else:
        return None, None

# Streamlit App 
st.title("Eventlog hochladen")

# Upload aufrufen
file_path, file_type = upload_eventlog()

# Ausgabe für weitere Verarbeitung
if file_path:
    st.write(f" Dateipfad: {file_path}")
    st.write(f" Dateityp: {file_type}")