import streamlit as st
from statistic_analysis.outlier_structur import outlier_structure

def show_structure_outliers(log):
    """
    Zeigt Ausreißer in der Struktur des Ereignisprotokolls im Streamlit-Interface an.

    :param log: Das Ereignisprotokoll als DataFrame.
    """

    st.subheader("❗️ Ausreißer - Struktur")

    outliers = outlier_structure(log)
    if not outliers:
        st.write("Keine strukturellen Ausreißer gefunden.")
        return  

    for category, indices in outliers.items():
        st.write(f"### Kategorie: {category}")
        if indices:
            outlier_df = log.loc[indices]
            st.dataframe(outlier_df, use_container_width=True)
        else:
            st.write("Keine Ausreißer in dieser Kategorie gefunden.")

