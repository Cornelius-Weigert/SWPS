# ==========================
# 6. Zeit-Analyse
# =======================

def duration_pro_case(log, case_col="case_id", time_col="timestamp"):
    if time_col not in log.columns:
        print("->>> Kein Timestamp gefunden - Zeit-Analyse übersprungen.")
        return
    
    #Sortieren
    df_sorted = log.sort_values(by=[case_col, time_col])

    #Durchlaufzeit pro Case
    durations = df_sorted.groupby(case_col)[time_col].agg(["first", "last"])
    #!!!
    durations["Dauer"] = durations["last"] - durations["first"]

    print("\nDurchschnittliche Prozessdauer:", durations["Dauer"].mean())
    print("Kürzeste Prozessdauer:", durations["Dauer"].min())
    print("Längste Prozessdauer:", durations["Dauer"].max())

   

    return durations
