# ========================
# 3. Häufigkeit Analyse
# ========================
def frequency(df, event_col="concept:name"):
    freq = df[event_col].value_counts().reset_index()
    freq.columns = ["Event", "Häufigkeit"]
    return freq
