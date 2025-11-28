
import pandas as pd
def compare_with_standardwert(log, standard, event_col="concept:name", value_col="Vslue"):


    if value_col not in log.columns:
        print(f"->>> Keine Spalte für Standardwert-Vergleich gefunden: {value_col}")
        return


    if isinstance(standard,(int, float, pd.Timedelta)):
        log["Standardwert"]=standard 
    else:
        if event_col is not None:
            log["Standardwert"] = log[event_col].map(standard)
       

    log["Abweichung"] = log[value_col] - log["Standardwert"]

    return log[[value_col, "Standardwert", "Abweichung"]]


    








'''
Datenanalyse_Outliers.statistic_analysis.standard_compare 的 Docstring
import pandas as pd

def compare_with_standardwert(log, event_col="concept:name", value_col="value"):
    
    """
    Standardwert und somit Abweichung von Event abrechnen
    Dataframe: Event, value, Standardwert, Abweichung 
    """

    # value column erkennen
    if value_col not in log.columns:
        print("->>> Keine Spalte gefunden für Standardwert-Vergleich:", value_col)
        return None

    # 1. Standardwert (Durchschnitt) abrechnen
    standardwerte = log.groupby(event_col)[value_col].mean()

    # 2. Standwert in log abbilden
    log["Standardwert"] = log[event_col].map(standardwerte)

    # 3️. Abweichung = value - Standardwert
    log["Abweichung"] = log[value_col] - log["Standardwert"]

    print("->>> Standardwert-Vergleich abgeschlossen")

    # return
    return log[[event_col, value_col, "Standardwert", "Abweichung"]]
    '''


