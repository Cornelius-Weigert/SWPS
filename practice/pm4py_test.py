import pm4py

def main():
    # use a raw string so backslashes are not treated as escapes
    log = pm4py.read_xes(r'C:\Users\Corne\Dokumente\studium\Semester 5\SWPS\practice\BPI_Challenge_2019.xes')

    # Discover the directly follows graph
    directly_follows_graph, start_activities, end_activities = pm4py.discover_dfg(log)
    bpmn= pm4py.discover_bpmn_inductive(log)
    # Visualize the DFG
    pm4py.view_dfg(directly_follows_graph, start_activities, end_activities,format='svg',graph_title="Directly Follows Graph")
    #pm4py.view_bpmn(bpmn,format='svg',graph_title="Hello World BPMN")

def get_dfg_image(log):
    directly_follows_graph, start_activities, end_activities = pm4py.discover_dfg(log)
    dfg_image = pm4py.view_dfg(directly_follows_graph, start_activities, end_activities,format='svg',graph_title="Directly Follows Graph")
    return dfg_image

def get_bpmn_image(log):
    bpmn= pm4py.discover_bpmn_inductive(log)
    bpmn_image = pm4py.view_bpmn(bpmn,format='svg',graph_title="Hello World BPMN")
    return bpmn_image

if __name__ == "__main__":
    main()