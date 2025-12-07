import streamlit as st
from statistic_analysis.outlier_trace import outlier_trace
def show_trace_outliers(log):
    """
    Zeigt Ausreißer in den Spuren des Ereignisprotokolls im Streamlit-Interface an.

    :param log: Das Ereignisprotokoll als DataFrame.
    """

    st.subheader("❗️ Ausreißer - Spuren")

    outliers = outlier_trace(log)

    for category, indices in outliers.items():
        st.write(f"### Kategorie: {category}")
        if indices:
            outlier_df = log.loc[indices]
            st.dataframe(outlier_df, use_container_width=True)
        else:
            st.write("Keine Ausreißer in dieser Kategorie gefunden.")
            