# Run instructions:
# 1) From the app directory (recommended):
#    cd "c:\Users\Corne\Dokumente\studium\Semester 5\SWPS\practice"
#    streamlit run streamlit-test.py
#
# 2) Or from any folder (quote the full path because it contains spaces):
#    streamlit run "c:\Users\Corne\Dokumente\studium\Semester 5\SWPS\practice\streamlit-test.py"
#    --or--
#    python -m streamlit run "c:\Users\Corne\Dokumente\studium\Semester 5\SWPS\practice\streamlit-test.py"
#
# 3) If using the project virtualenv, activate it first or run the venv python:
#    .venv\Scripts\Activate
#    streamlit run streamlit-test.py
#    --or--
#    .venv\Scripts\python -m streamlit run "c:\...\practice\streamlit-test.py"

import streamlit as st
from pm4py_test import get_bpmn_image
from pm4py_test import get_dfg_image

st.title("Hello, Streamlit!")
st.write("""*Hello World!*
         This is a simple Streamlit application.""")

# display BPMN and DFG images
# does not work yet, because st.image() needs a URL or file path, not an object
st.title("BPMN Visualization from XES Log")
#st.image(get_bpmn_image('C:/Users/Corne/Dokumente/studium/Semester 5/SWPS/practice/running-example.xes'))
st.title("Directly Follows Graph from XES Log")
#st.image(get_dfg_image('C:/Users/Corne/Dokumente/studium/Semester 5/SWPS/practice/running-example.xes'))