# ==========================
# 6. Zeit-Analyse
# =======================

def time_analysis(df, case_col="case:concept:name", time_col="time:timestamp"):
    if time_col not in df.columns:
        print("->>> Kein Timestamp gefunden – Zeit-Analyse übersprungen.")
        return
    
    #Sortieren
    df_sorted = df.sort_values(by=[case_col, time_col])

    #Durchlaufzeit pro Case
    durations = df_sorted.groupby(case_col)[time_col].agg(["first", "last"])
    #!!!
    durations["Dauer"] = durations["last"] - durations["first"]

    print("\n->>> Durchschnittliche Prozessdauer:", durations["Dauer"].mean())
    print("->>> Kürzeste Prozessdauer:", durations["Dauer"].min())
    print("->>> Längste Prozessdauer:", durations["Dauer"].max())

    return durations
