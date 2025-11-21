import pm4py
import datetime
import os

def main():
    log = pm4py.read_xes('Eventlogs/running-example.xes')   
    directly_follows_graph, start_activities, end_activities = pm4py.discover_dfg(log)
    
    pm4py.save_vis_dfg(directly_follows_graph, start_activities, end_activities, 'temp_graphs/'+str(datetime.date.today())+'_dfg.png')

def get_dfg_image(log,percentage=0.2):
    """Given an event log in PM4Py format, this function generates and saves a Directly Follows Graph (DFG) image in the 'temp_graphs' directory.
    Percentage parameter can be used to filter the DFG paths.
    It returns the svg code of the saved DFG image so that it can be displayed in the streamlit application."""
    dfg,sa,ea = pm4py.discover_dfg(log)
    dfg, sa, ea = pm4py.filtering.filter_dfg_paths_percentage(dfg,sa,ea,percentage)
    image_path = 'temp_graphs/'+str(datetime.date.today())+'_dfg.svg'
    pm4py.save_vis_dfg(dfg, sa, ea,image_path)
    with open(image_path,"r",encoding="utf-8") as image_file: svg_code = image_file.read()
    svg_code = svg_code[svg_code.find("<svg"):]
    os.remove(image_path)
    return svg_code

def get_bpmn_image(log, percentage=1):
    """Given an event log in PM4Py format, this function generates and saves a BPMN image in the 'temp_graphs' directory.
     It returns the svg code of the saved BPMN image so that it can be displayed in the streamlit application."""
    log = pm4py.filtering.filter_variants_by_coverage_percentage(log,1-percentage)
    bpmn = pm4py.discover_bpmn_inductive(log)
    image_path = 'temp_graphs/'+str(datetime.date.today())+'_bpmn.svg'
    pm4py.save_vis_bpmn(bpmn,image_path)
    with open(image_path,"r",encoding="utf-8") as image_file: svg_code = image_file.read()
    svg_code = svg_code[svg_code.find("<svg"):]
    os.remove(image_path)
    return svg_code

def get_main_process_dfg_image(log):
    return get_dfg_image(log,percentage=0.15)
def get_main_process_bpmn_image(log):
    return get_bpmn_image(log,percentage=0.95)

if __name__ == "__main__":
    main()