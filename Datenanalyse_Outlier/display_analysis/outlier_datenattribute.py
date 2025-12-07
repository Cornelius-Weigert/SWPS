import streamlit as st
from statistic_analysis.outlier_datenattribute import data_attribute_outliers

def show_datenattribute_outliers(log):
    
    st.subheader("❗️ Ausreißer - Datenattribute")

    
    attribute_cols = log.select_dtypes(include=['object', 'category']).columns.tolist()
    selected_col = st.selectbox("Spalte auswählen:", attribute_cols)

    outliers = data_attribute_outliers(log, attribute_col=selected_col)

    for category, indices in outliers.items():
        st.write(f"### Kategorie: {category}")
        if indices:
            outlier_df = log.loc[indices]
            st.dataframe(outlier_df, use_container_width=True)
        else:
            st.write("Keine Ausreißer in dieser Kategorie gefunden.")
