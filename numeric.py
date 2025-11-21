# ======================
# 4. Numerische Analyse
# =====================
def numeric(df, event_col="concept:name"):
    numeric_cols = df.select_dtypes(include="number").columns

    if len(numeric_cols) == 0:
        return None

    stats = df.groupby(event_col)[numeric_cols].agg(["mean", "std"])
    stats=stats.reset_index()
    return stats

