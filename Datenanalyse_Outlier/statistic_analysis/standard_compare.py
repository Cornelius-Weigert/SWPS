
import pandas as pd
def compare_with_standardwert(log, standard, event_col="activity", value_col="value"):


    if value_col not in log.columns:
        print(f"->>> Keine Spalte für Standardwert-Vergleich gefunden: {value_col}")
        return


    if isinstance(standard,(int, float, pd.Timedelta)):
        log["Standardwert"]=standard 
    else:
        if event_col is not None:
            log["Standardwert"] = log[event_col].map(standard)
       

    log["Abweichung"] = log[value_col] - log["Standardwert"]

    # Ergebnisse mit Vorzeichen formatiieren 
    if pd.api.types.is_timedelta64_dtype(log["Abweichung"]):
        def format_timedelta(td):
            sign = "+" if td >= pd.Timedelta(0) else "-"
            td_abs = abs(td)
            return f"{sign}{td_abs}"
        log["Abweichung_formatiert"] = log["Abweichung"].apply(format_timedelta)
    else:
        log["Abweichung_formatiert"] = log["Abweichung"].apply(lambda x: f"{x:+}")

    return log[[value_col, "Standardwert", "Abweichung", "Abweichung_formatiert"]]


    











