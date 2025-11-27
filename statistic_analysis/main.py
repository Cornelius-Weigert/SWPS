
from Datenanalyse_Outliers.statistic_analysis.reader import read_event_log
from Datenanalyse_Outliers.statistic_analysis.basic import basic_analysis
from Datenanalyse_Outliers.statistic_analysis.frequency import frequency
from Datenanalyse_Outliers.statistic_analysis.numeric import numeric
from Datenanalyse_Outliers.statistic_analysis.resources import resources
from Datenanalyse_Outliers.statistic_analysis.time_analysis import time_analysis
from Datenanalyse_Outliers.statistic_analysis.duration import duration_pro_activity
from Datenanalyse_Outliers.statistic_analysis.standard_compare import compare_with_standardwert
from Datenanalyse_Outliers.statistic_analysis.outlier_activity_duration import activity_duration_outliers
from Datenanalyse_Outliers.statistic_analysis.outlier_case_duration import case_duration_outliers
from Datenanalyse_Outliers.statistic_analysis.outlier_numeric import numeric_outliers



def full_log_analysis(path):
    #Datei einlesen
    df = read_event_log(path)

    #basisanalyse
    basic_analysis(df)

    #Häufigkeit
    freq = frequency(df)
    print("\n->>>Häufigkeit der Events:")
    print(freq)

    #Nummer analyse
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
    time_analysis(df)

    #Aktivitätdauer
    activity_durations = duration_pro_activity(df)

    #Outlier Analyse
    # -------- Outlier Detection --------
    print("\n==== OUTLIER ANALYSIS ====")

    # 1. Case Duration Outliers
    case_outliers, case_bounds = case_duration_outliers(time_analysis(df))
    print("\n->>> Case Duration Outliers:")
    print(case_outliers)

    # 2. Activity Duration Outliers
    activity_outliers, activity_bounds = activity_duration_outliers(activity_durations)
    print("\n->>> Activity Duration Outliers:")
    print(activity_outliers)

    # 3. Numeric Outliers (if value column exists)
    if "value" in df.columns:
        value_outliers, value_bounds = numeric_outliers(df, "value")
        print("\n->>> Numeric Outliers (value):")
        print(value_outliers)


    #?????????Standardwer-Vergleich???????????????????????????????
    standardwerte ={
        "a":3,
        "b":4,
        "c":5
    }
    compare_with_standardwert(df, standardwerte, value_col="value")

    return df, merged

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
df = full_log_analysis("event_log.xes")  # oder CSV
