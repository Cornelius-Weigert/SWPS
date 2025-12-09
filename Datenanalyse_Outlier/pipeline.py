
import pandas as pd
from .load_eventLog import eventLog_from_csv, eventLog_from_xes
from .eventlog_to_image import get_dfg_image
from Datenanalyse_Outlier.display_analysis.main import show_all_analysis
from .statistic_analysis import (
    reader, basic, numeric, resources, time_analysis,
    duration, standard_compare,
    outlier_activity_duration, outlier_case_duration, outlier_numeric, frequency
)
from .eventlog_to_dataframe import eventlog_to_df
from .map_columns import map_column

class AnalysisResult:
    def __init__(self, df, log, dfg_image):
        self.df = df
        self.log = log
        self.dfg_image = dfg_image

def run_analysis(file_path, file_type):
    """
    Führt das gesamte Datenanalyse-Pipeline aus:
    - Eventlog einlesen
    - Spalten vereinheitlichen
    - Statistik & Outlier Analyse
    - DFG Bild generieren
    """

    # --- 1️⃣ Eventlog einlesen ---
    if file_type.upper() == "CSV":
        df = pd.read_csv(file_path)
        df = map_column(df)
        log = eventLog_from_csv(file_path)
    elif file_type.upper() == "XES":
        log = eventLog_from_xes(file_path)
        df = eventlog_to_df(log)
        df = map_column(df)
    else:
        raise ValueError("Unbekannter Dateityp")

    # --- 2️⃣ Statistik / Outlier Analyse ---
    df = basic.basic_analysis(df)
    df = numeric.numeric_outliers(df)
    df = outlier_activity_duration.activity_duration_outliers(df)
    df = outlier_case_duration.case_duration_outliers(df)
    # Hier können weitere Analysen aus statistic_analysis hinzugefügt werden

    # --- 3️⃣ DFG Bild ---
    dfg_img = get_dfg_image(log)

    # --- 4️⃣ Ergebnis zurückgeben ---
    return AnalysisResult(df=df, log=log, dfg_image=dfg_img)
