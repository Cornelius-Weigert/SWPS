import pandas as pd
import pm4py

def eventLog_from_csv(path, separator=',', case_id='Case ID', activity_key='Activity', timestamp_key='Complete Timestamp'):
    """Load an event log from a CSV file and convert it to PM4Py event log format. path describes the file path to the CSV file.
    case_id, activity_key, and timestamp_key specify the column names for case ID, activity, and timestamp respectively.
    This function returns the event log in PM4Py format."""
    dataframe = pd.read_csv(path, sep=separator)
    dataframe = pm4py.format_dataframe(dataframe, case_id=case_id, activity_key=activity_key, timestamp_key=timestamp_key)
    log = pm4py.convert_to_event_log(dataframe)
    return log

def eventLog_from_xes(path):
    """Load an event log from an XES file. path describes the file path to the XES file. 
    This function returns the event log in PM4Py format."""
    log = pm4py.read_xes(path)
    return log

def main():
    log = eventLog_from_csv('Eventlogs/eventlog.csv')
    dfg,sa,ea = pm4py.discover_dfg(log)
    dfg,sa,ea = pm4py.filtering.filter_dfg_paths_percentage(dfg,sa,ea,percentage=0.08)
    pm4py.view_dfg(dfg,sa,ea,format='svg',graph_title="Directly Follows Graph from CSV Log")
    log2 = eventLog_from_xes('Eventlogs/running-example.xes')
    dfg2,sa2,ea2 = pm4py.discover_dfg(log2)
    pm4py.view_dfg(dfg2,sa2,ea2,format='svg',graph_title="Directly Follows Graph from XES Log")

if __name__ == "__main__":
    main()
