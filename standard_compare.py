# ==========================
# 7. Standardwerte-Vergleich
# =======================
def compare_with_standardwert(df, standard, event_col="concept:name", value_col="value"):
    if value_col not in df.columns:
        print("->>> Keine Spalte für Standardwert-Vergleich gefunden:", value_col)
        return

   #Standard Spalte hinzufügen
    df["Standardwert"] = df[event_col].map(standard)
   #Abweichung hinzufügen
    df["Abweichung"] = df[value_col] - df["Standardwert"]

    print("->>>Standardwert-Vergleich abgeschlossen")
    return df[[event_col, value_col, "Standardwert", "Abweichung"]]
