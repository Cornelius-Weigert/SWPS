import pm4py
import pandas as pd
import matplotlib.pyplot as plt
import os

# ===========================
# 1. Datei automatisch lesen
# ===========================
def read_event_log(path):
    ext = os.path.splitext(path)[1].lower()

    if ext == ".xes":
        log= pm4py.read_xes(path)
    elif ext == ".csv":
        log= pm4py.read_csv(path)
    else: print("Nur CSV- und XES-Datei akzeptiert")    

    return pm4py.convert_to_dataframe(log)


# ===================
# 2. Basis-Analyse
# ===================
def basic_analysis(df):
    print("->>>Verfügbare Spalten:", list(df.columns))
    print("\n->>> Kopf der Daten:")
    print(df.head())
    print("\n------------------------")


# ========================
# 3. Häufigkeit Analyse
# ========================
def frequency(df, event_col="concept:name"):
    freq = df[event_col].value_counts().reset_index()
    freq.columns = ["Event", "Häufigkeit"]
    return freq


# ======================
# 4. Numerische Analyse
# =====================
def numeric(df, event_col="concept:name"):
    numeric_cols = df.select_dtypes(include="number").columns

    if len(numeric_cols) == 0:
        return None

    stats = df.groupby(event_col)[numeric_cols].agg(["mean", "std"])
    stats = stats.reset_index()
    return stats


# ======================
# 5. Resource / String Analyse mit Diagramm
# ===========================
def resources(df, event_col="concept:name", resource_col="org:resource"):
    if resource_col not in df.columns:
        print("->>>Keine Ressourcenspalten gefunden")
    
    activities = df[event_col].unique()

    for act in activities:
        sub = df[df[event_col] == act]
        counts = sub[resource_col].value_counts()

        plt.figure(figsize=(7, 4))
        counts.plot(kind="bar")

        plt.title(f"Ressourcen für Aktivität: {act}")
        plt.xlabel("Resource")
        plt.ylabel("Menge")

        plt.tight_layout()
        plt.show()


# ==========================
# 6. Zeit-Analyse
# =======================
def time(df, case_col="case:concept:name", time_col="time:timestamp"):
    if time_col not in df.columns:
        print("->>> Kein Timestamp gefunden – Zeit-Analyse übersprungen.")
        return

    # Sortieren
    df_sorted = df.sort_values(by=[case_col, time_col])

    # Durchlaufzeit pro Case
    durations = df_sorted.groupby(case_col)[time_col].agg(["first", "last"])
    #!!!
    durations["Dauer"] = durations["last"] - durations["first"]

    print("\n->>> Durchschnittliche Prozessdauer:", durations["Dauer"].mean())
    print("->>> Kürzeste Prozessdauer:", durations["Dauer"].min())
    print("->>> Längste Prozessdauer:", durations["Dauer"].max())

    return durations

#===========================
#7. Standardwert und Vergleich
#============================
def compare_with_standardwert(df, stand, event_col="concept:name",value_col="value"):
    if value_col not in df.columns:
        print("->>>Keine Spalte für Standardwert-Vergleich fgefunden:", value_col)
        return
    
 #Standard Spalte hinzufügen
    df["Standardwert"] = df[event_col].map(standard)

 #Abweichung hinzufügen
    df["Abweichung"]=df[value_col]-df["Standardwert"]

    print("->>>Standardwert-Vergleich abgeschlossen")
    return df[[event_col, value_col, "Standardwert", "Abweichung"]]


#=======================
#Benötige Zeit pro Aktivität
#========================
def duration_pro_activity(df, case_col="case:concept:name", event_col="concept:name",time_col="time:timestamp"):
    if time_col not in df.columns:
        print("->>>Keine Timestamp - Aktivitätsdauer Analyse übersprungen.")
        return

    df_sorted =df.sort_values(by=[case_col,time_col])   

#next
    df_sorted["next_time"]= df_sorted.groupby(case_col)[time_col].shift(-1)

#duration
    df_sorted["Activity_Duration"]=df_sorted["next_time"]-df_sorted[time_col]

#durchschnitt
    activity_durations =df_sorted.groupby(event_col)["Activity_Duration"].mean().reset_index()
    print("\n->>> Durchschnittliche Dauer pro Aktivität:")
    print(activity_durations)


# =======================
# 9. "Main-Methode"
# ========================
def full_log_analysis(path):

    # Datei einlesen
    df = read_event_log(path)

    # Basisanalyse
    basic_analysis(df)

    # Häufigkeiten
    freq = frequency(df)
    print("\n->>>Häufigkeit der Events:")
    print(freq)

    # Nummer Analyse
    numeric_stats = numeric(df)
    if numeric_stats is not None:
        print("\n->>> Numerische Statistik:")
        print(numeric_stats)
        merged = pd.merge(freq, numeric_stats, left_on="Event", right_on="concept:name", how="left")
    else:
        merged = freq

    print("\n->>> Zusammenfassung:")
    print(merged)

    # Ressourcenanalyse (mit Plot)
    print("\n->>> Erstelle Ressourcen-Diagramme…")
    if "org:resource" in df.columns:
        resources(df)
    else:
        print("->>> Keine Ressourcenspalte (`org:resource`) gefunden.")

    # Zeit-Analyse
    time(df)

    #Aktivitätdauer
    activity_durations = duration_pro_activity(df)

    #Standardwer-Vergleich
    #???????????????????????????????
    standardwerte ={
        "a":3,
        "b":4,
        "c":5
    }
    compare_with_standardwert(df, standardwerte, value_col="value")

    return df, merged

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
df = full_log_analysis("event_log.xes") 

