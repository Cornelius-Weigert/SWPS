import pandas as pd
import pm4py

def eventLog_from_csv(path, separator=',', case_id='Case ID', activity_key='Activity', timestamp_key='Complete Timestamp'):
    dataframe = pd.read_csv(path, sep=',')
    dataframe = pm4py.format_dataframe(dataframe, case_id=case_id, activity_key=activity_key, timestamp_key=timestamp_key)
    log = pm4py.convert_to_event_log(dataframe)
    return log

def eventLog_from_xes(path):
    log = pm4py.read_xes(path)
    return log

def main():
    log = eventLog_from_csv('Eventlogs/eventlog.csv')
    dfg,sa,ea = pm4py.discover_dfg(log)
    pm4py.view_dfg(dfg,sa,ea,format='svg',graph_title="Directly Follows Graph from CSV Log")

if __name__ == "__main__":
    main()
