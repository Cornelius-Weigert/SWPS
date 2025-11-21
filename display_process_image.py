import streamlit as st
import eventlog_to_image 
import load_eventLog
import re

log = load_eventLog.eventLog_from_csv('Eventlogs/eventlog.csv')

st.title("Filter the process variants in the event log")

percentage_slider = st.slider("What percentage of the variants do you want to keep?",0.0,1.0,step=0.01)

# display DFG images

st.title("Directly Follows Graph from XES Log")
st.image(eventlog_to_image.get_dfg_image(log,percentage=percentage_slider))