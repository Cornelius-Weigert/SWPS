import pm4py
import datetime

def main():
    log = pm4py.read_xes('Eventlogs/running-example.xes')   
    directly_follows_graph, start_activities, end_activities = pm4py.discover_dfg(log)
    
    pm4py.save_vis_dfg(directly_follows_graph, start_activities, end_activities, 'temp_graphs/'+str(datetime.datetime())+'_dfg.png')

def get_dfg_image(log):
    directly_follows_graph, start_activities, end_activities = pm4py.discover_dfg(log)
    image_path = 'temp_graphs/'+str(datetime.date.today())+'_dfg.png'
    pm4py.save_vis_dfg(directly_follows_graph, start_activities, end_activities,image_path)
    return image_path

def get_bpmn_image(log):
    bpmn = pm4py.discover_bpmn_inductive(log)
    image_path = 'temp_graphs/'+str(datetime.date.today())+'_bpmn.png'
    pm4py.save_vis_bpmn(bpmn,image_path)
    return image_path

if __name__ == "__main__":
    main()