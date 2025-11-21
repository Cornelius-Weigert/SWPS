import pandas as pd

# ---------------------------------------
# 2. Activity Duration Outliers
# ---------------------------------------
def activity_duration_outliers(df, duration_col="Activity_Duration"):
    """Detect outliers in activity durations."""
    df2 = df.copy()

    # convert timedelta to seconds
    df2["sec"] = df2[duration_col].dt.total_seconds()

    Q1 = df2["sec"].quantile(0.25)
    Q3 = df2["sec"].quantile(0.75)
    IQR = Q3 - Q1

    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR

    outliers = df2[(df2["sec"] < lower) | (df2["sec"] > upper)]
    return outliers, (lower, upper)

