import pm4py
import os

# ===========================
# 1. Datei automatisch lesen
# ===========================
def read_event_log(path):
    ext = os.path.splitext(path)[1].lower()
    
    if ext == ".xes":
        log = pm4py.read_xes(path)
    elif ext == ".csv":
        log = pm4py.read_csv(path)
    else:
        raise ValueError("Nur CSV- und XES-Datei akzeptiert")    

    return pm4py.convert_to_dataframe(log)
