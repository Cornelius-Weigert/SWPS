import pandas as pd

# ---------------------------------------
# 2. Activity Duration Outliers
# ---------------------------------------
def activity_duration_outliers(log, duration_col="Activity_Duration", lower1=0.10, upper1=0.90, factor=1.5  ):
    """Detect outliers in activity durations."""
    df2 = log.copy()

    # convert timedelta to seconds
    df2["sec"] = df2[duration_col].dt.total_seconds()

    Q1 = df2["sec"].quantile(lower1)
    Q3 = df2["sec"].quantile(upper1)
    IQR = Q3 - Q1

    lower = Q1 - factor * IQR
    upper = Q3 + factor  * IQR

    outliers = df2[(df2["sec"] < lower) | (df2["sec"] > upper)]
    return outliers, (lower, upper)

