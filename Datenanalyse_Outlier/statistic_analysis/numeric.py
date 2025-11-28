# ======================
# 4. Numerische Analyse
# =====================
def numeric1(log, event_col="concept:name"):
    numeric_cols = log.select_dtypes(include="number").columns

    if len(numeric_cols) == 0:
        return None

    stats = log.groupby(event_col)[numeric_cols].agg(["mean", "std"])
    stats=stats.reset_index()
    return stats

