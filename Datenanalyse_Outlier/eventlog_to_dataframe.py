
import pandas as pd
from pm4py.objects.log.obj import EventLog, Trace, Event
import pm4py


def eventlog_to_df(log):
    # 1.bereits DataFrame -> direkt zurückgeben
    if isinstance(log, pd.DataFrame):
        print("DEBUG: Input ist bereits DataFrame")
        return log
    

    # 2.falls XES -> in DataFrame 
    if isinstance(log, EventLog):
        print("DEBUG: EventLog erkannt, konvertiere...")

        rows = []
        for trace in log:
            for event in trace:
                if isinstance(event, dict):
                    rows.append(event)
                elif hasattr(event, "keys"):
                    rows.append(dict(event))
                else:
                    print("WARNUNG: Ungültiges Event:", event)

        log = pd.DataFrame(rows)
        return log

    # Unbekannter Typ
    print("ERROR: log hat unbekannten Typ:", type(log))
    return None
