import streamlit as st
import eventlog_to_image 
import load_eventLog
import re

log = load_eventLog.eventLog_from_csv('Eventlogs/eventlog.csv')

st.title("Hello, Streamlit!")
st.write("""*Hello World!*
         This is a simple Streamlit application.""")

# display BPMN and DFG images
st.title("BPMN Visualization from XES Log")
st.image(eventlog_to_image.get_bpmn_image(log,percentage=0.95))


st.title("Directly Follows Graph from XES Log")
st.image(eventlog_to_image.get_dfg_image(log,percentage=0.15))