import pandas as pd

# ---------------------------------------
# 1. Case Duration Outliers
# ---------------------------------------
def case_duration_outliers(durations):
    """Detect outliers in total process duration per case."""
    df = durations.copy()
    df["Dauer_sec"] = df["Dauer"].dt.total_seconds()

    Q1 = df["Dauer_sec"].quantile(0.25)
    Q3 = df["Dauer_sec"].quantile(0.75)
    IQR = Q3 - Q1

    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR

    outliers = df[(df["Dauer_sec"] < lower) | (df["Dauer_sec"] > upper)]
    return outliers, (lower, upper)

