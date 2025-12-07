import streamlit as st
from statistic_analysis.outlier_temporal import temporal_outliers
import pandas as pd


def deduplicate_columns(log):
    new_cols = []
    seen = {}
    for col in log.columns:
        if col in seen:
            seen[col] += 1
            new_cols.append(f"{col}_{seen[col]}")
        else:
            seen[col] = 0
            new_cols.append(col)
    log.columns = new_cols
    return log


def show_temporal_outliers(log):

    st.subheader("❗️ Ausreißer - Zeitlich")

    log = deduplicate_columns(log)

    outliers = temporal_outliers(log)

    for category, indices in outliers.items():
        st.write(f"### Kategorie: {category}")
        if indices:
            outlier_df = log.loc[indices]
            st.dataframe(outlier_df, use_container_width=True)
        else:
            st.write("Keine Ausreißer in dieser Kategorie gefunden.")
        