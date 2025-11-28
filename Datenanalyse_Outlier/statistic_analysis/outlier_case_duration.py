

import pandas as pd

# ---------------------------------------
# 1. Case Duration Outliers
# ---------------------------------------
def case_duration_outliers(durations):
    """Detect outliers in total process duration per case."""
    log = durations.copy()
    log["Dauer_sec"] = log["Dauer"].dt.total_seconds()

    Q1 = log["Dauer_sec"].quantile(0.25)
    Q3 = log["Dauer_sec"].quantile(0.75)
    IQR = Q3 - Q1

    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR

    outliers = log[(log["Dauer_sec"] < lower) | (log["Dauer_sec"] > upper)]
    return outliers, (lower, upper)
