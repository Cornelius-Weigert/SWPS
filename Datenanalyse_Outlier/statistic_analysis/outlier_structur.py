import pandas as pd
def outlier_structure(log, case_col="case_id", activity_col="activity"):
    """
    Identifiziert strukturelle Ausreißer im Ereignisprotokoll basierend auf der Anzahl der Aktivitäten pro Fall.

    Parameter:
    log (pd.DataFrame): Das Ereignisprotokoll als DataFrame.
    case_col (str): Name der Spalte für Fall-IDs.
    activity_col (str): Name der Spalte für Aktivitäten.

    Rückgabe:
    dict: Ein Dictionary mit Kategorien als Schlüsseln und Listen von Indizes der Ausreißer als Werten.
    """
    outliers = {}

    #+++++++Wenn ein Fall keine Aktivitäten hat+++++++++++++
    case_activity_counts = log.groupby(case_col)[activity_col].nunique()
    no_activity_cases = case_activity_counts[case_activity_counts == 0].index
    no_activity_rows = log[log[case_col].isin(no_activity_cases)]
    outliers['no-activity-cases'] = no_activity_rows.index.tolist()   

    #+++++++Wenn ein Fall ungewöhnlich viele Aktivitäten hat+++++++++++++
    high_activity_cases = case_activity_counts[case_activity_counts > case_activity_counts.quantile(0.95)].index
    high_activity_rows = log[log[case_col].isin(high_activity_cases)]
    outliers['high-activity-cases'] = high_activity_rows.index.tolist()   

    #+++++++Wenn ein Fall ungewöhnlich wenige Aktivitäten hat+++++++++++++
    low_activity_cases = case_activity_counts[case_activity_counts < case_activity_counts.quantile(0.05)].index
    low_activity_rows = log[log[case_col].isin(low_activity_cases)]
    outliers['low-activity-cases'] = low_activity_rows.index.tolist()   

    