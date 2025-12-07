

import pandas as pd

# ---------------------------------------
# 1. Case Duration Outliers
# ---------------------------------------
def case_duration_outliers(durations, lower1=0.10, upper1=0.90, factor=1.5):
    """Detect outliers in total process duration per case."""
    log = durations.copy()
    log["Dauer_sec"] = log["Dauer"].dt.total_seconds()

    Q1 = log["Dauer_sec"].quantile(lower1)
    Q3 = log["Dauer_sec"].quantile(upper1)
    IQR = Q3 - Q1

    lower = Q1 - factor * IQR
    upper = Q3 + factor * IQR

    outliers = log[(log["Dauer_sec"] < lower) | (log["Dauer_sec"] > upper)]
    return outliers, (lower, upper)
