# ========================
# 3. Häufigkeit Analyse
# ========================
def frequency1(log, event_col="concept:name"):
    freq = log[event_col].value_counts().reset_index()
    freq.columns = ["Event", "Häufigkeit"]
    return freq
