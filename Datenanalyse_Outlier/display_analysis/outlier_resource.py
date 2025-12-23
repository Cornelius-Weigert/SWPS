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
    factor_res = st.session_state.get('factor_res') #= 1.5
    if show_res_slider:   
        st.write("Perzentilebasierte Grenzenwerte(Anzahl durchgefürten Aktivitäten pro Resource) ")
        lower_res = st.slider("Untere Grenze (Resource)", 0.0, 0.5, lower_res, 0.01,help="Der Anzahl von Aktivitäten, der die Resourcen so teilt, dass x% der Resourcen weniger oder gleich diesem Wert treiben(und y% mehr)")
        upper_res = st.slider("Obere Grenze (Resource)", 0.5, 1.0, upper_res, 0.01,help="Der Anzahl von Aktivitäten, der die Resourcen so teilt, dass y% der Resourcen weniger oder gleich diesem Wert treiben(und x% mehr)")
        factor_res = st.slider("Faktor (Resource)", 1.0, 5.0,factor_res, 0.1,help="Ein häufig verwendeter Faktor (meist 1,5), um Ausreißer zu identifizieren")
        st.session_state['lower_res'] = lower_res
        st.session_state['upper_res'] = upper_res
        st.session_state['factor_res'] = factor_res

    display_cols=["case_id","activity","resource","timestamp"]

    outliers,log_with_counts = outlier_resources(log_df)

    resource_activity_count = log_df.groupby("resource").size().reset_index(name="resource_activity_count")
    resource_unique_activity_counts = log_df.groupby("resource")["activity"].nunique().reset_index(name="unique_activity_count")

    for category, indices in outliers.items():
        st.write(f"### Kategorie: {category}")
        if category in OUTLIER_DESCRIPTIONS:
            st.caption(OUTLIER_DESCRIPTIONS[category]["description"])

        if indices:
            outlier_df = log_df.loc[indices, display_cols]

            if category == "diverse-activity-resources":
                outlier_df = outlier_df.merge(
                    resource_unique_activity_counts,
                    on="resource",
                    how="left"
                )
            else:
                outlier_df = outlier_df.merge(
                    resource_activity_count,
                    on="resource",
                    how="left"
                )

            selectable_outliers = st.dataframe(
                outlier_df, 
                width="stretch",
                on_select="rerun",
                selection_mode="multi-row",
                hide_index=True)
            comment = st.text_area("(optional) Kommentar zu ausgewählten Ausreißern eingeben",key=f"comment_temporal_{category}")
            ausreißer_akzeptiert_button = st.button("Ausgewählte Ausreißer akzeptieren", key=f"accept_temporal_{category}")
            if ausreißer_akzeptiert_button:
                accept_outliers(selectable_outliers.selection.rows,category,outlier_df,comment,"resource")
                selectable_outliers.selection.clear()
        else:
            st.write("Keine Ausreißer in dieser Kategorie gefunden.")

