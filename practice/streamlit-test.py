import streamlit as st
import eventlog_to_image 
import pm4py

log = pm4py.read_xes('Eventlogs/BPI_Challenge_2019.xes')

st.title("Hello, Streamlit!")
st.write("""*Hello World!*
         This is a simple Streamlit application.""")

# display BPMN and DFG images
st.title("BPMN Visualization from XES Log")
st.image(eventlog_to_image.get_bpmn_image(log))

st.title("Directly Follows Graph from XES Log")
st.image(eventlog_to_image.get_dfg_image(log))