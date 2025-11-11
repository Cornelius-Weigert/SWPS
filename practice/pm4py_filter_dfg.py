import pm4py

def path_percentage_filtered_dfg(dfg,start_activities,end_activities):
    percentage = 0.06
    filtered_dfg, filtered_start_activities, filtered_end_activities = pm4py.filtering.filter_dfg_paths_percentage(dfg,start_activities,end_activities,percentage)
    pm4py.view_dfg(filtered_dfg, filtered_start_activities, filtered_end_activities, format='svg',graph_title="path percentage filtered DFG")

def activity_percentage_filtered_dfg(dfg,start_activities,end_activities):
    percentage = 0.05
    activities_count = pm4py.statistics.attributes.log.get.get_attribute_values(log,'Activity')
    filtered_dfg, filtered_start_activities, filtered_end_activities = pm4py.filtering.filter_dfg_paths_percentage(dfg,start_activities,end_activities,percentage)
    pm4py.view_dfg(filtered_dfg, filtered_start_activities, filtered_end_activities, format='svg',graph_title="activity percentage filtered DFG")


log = pm4py.read_xes('Eventlogs/BPI_Challenge_2019.xes')
log2 = pm4py.read_xes('Eventlogs/running-example.xes')

directly_follows_graph, start_activities, end_activities = pm4py.discover_dfg(log)

# path_percentage_filtered_dfg(directly_follows_graph,start_activities,end_activities)
activity_percentage_filtered_dfg(directly_follows_graph,start_activities,end_activities)