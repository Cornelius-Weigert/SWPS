import pandas as pd

# ---------------------------------------
# 3. Numeric Outliers
# ---------------------------------------
def numeric_outliers(df, value_col):
    """Detect outliers in any numeric column."""
    Q1 = df[value_col].quantile(0.25)
    Q3 = df[value_col].quantile(0.75)
    IQR = Q3 - Q1

    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR

    outliers = df[(df[value_col] < lower) | (df[value_col] > upper)]
    return outliers, (lower, upper)
