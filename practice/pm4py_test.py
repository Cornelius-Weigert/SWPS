import pm4py
import tempfile
import os

def main():
    log = pm4py.read_xes('Eventlogs/BPI_Challenge_2019.xes')
    log2 = pm4py.read_xes('Eventlogs/running-example.xes')
    # print(get_dfg_image(log2))
    # script_dir = os.getcwd()
    # temp_path = os.path.join(script_dir, 'temp_graphs')
    # os.makedirs(temp_path, exist_ok=True)
    # with tempfile.NamedTemporaryFile(delete=False,suffix='.svg',dir=temp_path) as fd:
    #     path = fd.name
    # # print(fd.name)
    # print(path)
    
    # Discover the directly follows graph
    directly_follows_graph, start_activities, end_activities = pm4py.discover_dfg(log)
    dfg, sa, ea = pm4py.filtering.filter_dfg_activities_percentage(directly_follows_graph, start_activities, end_activities, percentage=0.25)
    pm4py.vis.save_vis_performance_dfg(dfg, sa, ea,'temp_graphs/performance_dfg.svg')
    # bpmn= pm4py.discover_bpmn_inductive(log)
    # Visualize the DFG
    # pm4py.view_dfg(directly_follows_graph, start_activities, end_activities,format='svg',graph_title="Directly Follows Graph")
    # pm4py.view_bpmn(bpmn,format='svg',graph_title="Hello World BPMN")
    # filtered_dfg, filtered_start_activities, filtered_end_activities = get_filtered_dfg(directly_follows_graph, start_activities, end_activities)
    # pm4py.view_dfg(filtered_dfg, filtered_start_activities, filtered_end_activities, format='svg')

    # attributes_count = pm4py.statistics.attributes.log.get.get_attribute_values(log,'Activity')
    # filtered_dfg, filtered_start_activities, filtered_end_activities, new_count = pm4py.algo.filtering.dfg.dfg_filtering.filter_dfg_keep_connected(directly_follows_graph,start_activities,end_activities,attributes_count,1000000)
    # pm4py.view_dfg(filtered_dfg, filtered_start_activities, filtered_end_activities, format='svg')
    # attributes_count = pm4py.statistics.attributes.log.get.get_attribute_values(log2, all_attributes)
    # print(attributes_count)

# def get_filtered_dfg(dfg,start_activity,end_activity):
#    dfg_new, start_activity_new, end_activity_new = pm4py.algo.filtering.dfg.dfg_filtering.filter_dfg_keep_connected(dfg,start_activity,end_activity,30,0.5)
#    return dfg_new, start_activity_new, end_activity_new

def get_dfg_image(log):
    script_dir = os.getcwd()
    temp_path = os.path.join(script_dir, 'temp_graphs')
    os.makedirs(temp_path, exist_ok=True)
    with tempfile.NamedTemporaryFile(delete=False,suffix='.png',dir=temp_path) as fd:
        path = fd.name
    directly_follows_graph, start_activities, end_activities = pm4py.discover_dfg(log)
    pm4py.algo.filtering.dfg.dfg_filtering.filter_dfg_on_path_percentage(directly_follows_graph,start_activities,end_activities,)
    # pm4py.save_vis_dfg(directly_follows_graph, start_activities, end_activities,path,max_num_edges=30,format='png',graph_title="Directly Follows Graph")
    pm4py.visualization.common.save.save(pm4py.visualization.dfg.visualizer.apply(directly_follows_graph,log,variant="frequency"),path)
    return path

def get_bpmn_image(log):
    bpmn= pm4py.discover_bpmn_inductive(log)
    bpmn_image = pm4py.view_bpmn(bpmn,format='svg',graph_title="Hello World BPMN")
    return bpmn_image

if __name__ == "__main__":
    main()