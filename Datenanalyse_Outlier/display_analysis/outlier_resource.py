import streamlit as st
from ..statistic_analysis.outlier_resource import outlier_resources
from .outlier_acception import accept_outliers
from.description import OUTLIER_DESCRIPTIONS

def show_resource_outliers(log_df):
    """
    Show resource outlier analysis in the Streamlit interface.
    Args: 
        log_df (pd.DataFrame): The event log as a DataFrame.
    Returns:
        None
    """
    #filter
    st.subheader("🌟 Filter - Resource_Activity Value")
    show_res_slider = st.checkbox("Perzentilebasierte Grenzwerte anzeigen ", value = False,key="resource_slider")
    lower_res = st.session_state.get('lower_res') #= 0.05
    upper_res = st.session_state.get('upper_res') #= 0.95
    upper_res_diverse=st.session_state.get('upper_res_diverse')
    factor_res = st.session_state.get('factor_res') #= 1.5

    if show_res_slider:   
        st.write("Perzentilebasierte Grenzenwerte(Anzahl durchgefürten Aktivitäten pro Resource) ")
        lower_res = st.slider("Untere Grenze (Ressource-wenig-aktiv)", 0.0, 0.5, lower_res, 0.01,help="Bestimmt das untere Perzentil der Anzahl ausgeführter Aktivitäten pro Ressource. Ressourcen unterhalb dieses Werts werden als potenzielle Ausreißer mit ungewöhnlich geringer Aktivitätsauslastung betrachtet.")
        upper_res = st.slider("Obere Grenze (Ressource-sehr-aktiv)", 0.5, 1.0, upper_res, 0.01,help="Bestimmt das obere Perzentil der Anzahl ausgeführter Aktivitäten pro Ressource. Ressourcen oberhalb dieses Werts werden als potenzielle Ausreißer mit ungewöhnlich hoher Aktivitätsauslastung betrachtet.")
        upper_res_diverse=st.slider("Obere Grenze (Ressource-vielfältige-Aktivitäten)",0.5,1.0,upper_res_diverse,0.01,help="Legt das Perzentil fest, ab dem Ressourcen als Ausreißer gelten, weil sie eine ungewöhnlich große Anzahl unterschiedlicher Aktivitäten ausführen. Beispiel: 0,95 bedeutet, dass nur die 5 % der Ressourcen mit der höchsten Aktivitätsvielfalt als Ausreißer markiert werden.")
        factor_res = st.slider("Faktor (Ressource)", 1.0, 5.0,factor_res, 0.1,help="Multiplikativer Faktor zur Feinjustierung der Ausreißererkennung. Höhere Werte führen zu einer strengeren, niedrigere Werte zu einer sensibleren Identifikation von Ausreißern. (Ein häufig verwendeter Faktor ist 1,5)")
        
        st.session_state['lower_res'] = lower_res
        st.session_state['upper_res'] = upper_res
        st.session_state['factor_res'] = factor_res
        st.session_state['upper_res_diverse']=upper_res_diverse

    display_cols=["case_id","activity","resource","timestamp"]

    outliers,log_with_counts = outlier_resources(log_df)

    resource_activity_count = log_df.groupby("resource").size().reset_index(name="resource_activity_count")
    resource_unique_activity_counts = log_df.groupby("resource")["activity"].nunique().reset_index(name="unique_activity_count")

    for category, indices in outliers.items():
        st.write(f"### Kategorie: {category}")
        if category in OUTLIER_DESCRIPTIONS:
            st.caption(OUTLIER_DESCRIPTIONS[category]["description"])

        if not indices:
            st.write("Keine Ausreißer in dieser Kategorie gefunden.")
            continue

        if category == "Ressource_vielfältige_Aktivitäten":
            temp_df= log_df.loc[indices, display_cols]
            outlier_df= temp_df.merge(resource_unique_activity_counts,on="resource", how="left")
            temp_col="unique_activity_count"
            label="Anzahl unterschiedlicher Aktivitäten:"
        else:
            temp_df=log_df.loc[indices, display_cols]
            outlier_df= temp_df.merge(resource_activity_count,on="resource", how="left")
            temp_col="resource_activity_count"
            label="Anzahl ausgeführter Aktivitäten:"

        for resource, res_df in outlier_df.groupby("resource"):
            value = res_df[temp_col].iloc[0]
            key_df=f"df_{category}_{resource}"
            key_comment=f"comment_{category}_{resource}"
            key_button=f"accept_{category}_{resource}"

            res_df_display=res_df[["case_id","activity","timestamp"]]
            with st.expander(
                f"👤 Ressource: {resource} ({label} {value})",
                expanded=False
            ):

                selectable_outliers = st.dataframe(
                res_df_display,
                key=key_df,
                width="stretch",
                on_select="rerun",
                selection_mode="multi-row",
                hide_index=True)
                comment = st.text_area("(optional) Kommentar zu ausgewählten Ausreißern eingeben",key=key_comment)
                ausreißer_akzeptiert_button = st.button("Ausgewählte Ausreißer akzeptieren", key=key_button)
                if ausreißer_akzeptiert_button:
                    accept_outliers(selectable_outliers.selection.rows,category,outlier_df,comment,"resource")
                    selectable_outliers.selection.clear()


    

