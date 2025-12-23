import graphviz
import streamlit as st
from ..statistic_analysis.outlier_trace import outlier_trace
from ..statistic_analysis.duration_process import duration_pro_case
from .outlier_acception import accept_outliers
from ..statistic_analysis.second_to_time import second_to_time
from ..statistic_analysis.duration_activity import duration_pro_activity
from ..statistic_analysis import duration_process
from .description import OUTLIER_DESCRIPTIONS

def create_trace_graph(log_df):
    graph = graphviz.Digraph()
    graph.attr("node", shape='box')
    for i in range(1, len(log_df["activity"])):
        graph.edge(log_df["activity"].iloc[i-1], log_df["activity"].iloc[i])
    return graph

# fragment for single trace so that only this part reruns on interaction -> improves performance
@st.fragment
def _render_single_trace(category, case_id, case_df):
    """Fragment for a single trace - only this trace reruns on checkbox click."""
    case_duration=second_to_time(case_df["case_duration"].iloc[0])
    with st.expander(f"Trace von Case ID: {case_id} | Case_Dauer: {case_duration}"):
        st.dataframe(case_df[
                ["activity","resource","timestamp","Activity_Duration_time"]]
            , width="stretch",hide_index=True)
        # Trace visualisieren, wenn ein Button geklickt wird
        trace_visualize_button = st.button("Trace visualisieren",key=f"visualize_trace_{case_id}_{category}")
        if trace_visualize_button:
            st.graphviz_chart(create_trace_graph(case_df))
        # Akzeptieren Button für Ausreißer
        comment = st.text_area("(Optional) Kommentar zu diesem Ausreißer eingeben",key=f"comment_trace_outliers_{case_id}_{category}")
        accept_comment = st.button("Kommentar bestätigen & Ausreißer akzeptieren", key=f"confirm_accept_trace_{case_id}_{category}")
        if accept_comment:
            # ToDo add outlier logic
            case_df["Kommentar"] = comment
            st.session_state["trace_outliers_accepted"].append([category,case_df])
            st.success(f"✅ Ausreißer für Case ID '{case_id}' in der Kategorie '{category}' wurde akzeptiert.") 


def show_trace_outliers(log_df):
    """
    Show trace outlier analysis in the Streamlit interface.
    Args:
        log_df (pd.DataFrame): The event log as a DataFrame.
    Returns:    
        None
    """
    #filter
    st.subheader("🌟 Filter - Case Duration")
    case_duration = duration_process.duration_pro_case(log_df)
    show_case_slider = st.checkbox("Perzentilebasierte Grenzwerte anzeigen ", value = False,key="case_slider")
    lower_case=st.session_state['lower_case']
    upper_case=st.session_state['upper_case']
    factor_case=st.session_state['factor_case']
    if show_case_slider:
            st.write("Perzentilebasierte Grenzenwerte(Case Duration)")
            lower_case = st.slider("Untere Grenze (Case)", 0.0, 0.5, lower_case, 0.01,help="Der Anzahl von Case-Dauer, der die Dauern so teilt, dass x% der Dauern kürzer oder gleich diesem Wert treiben(und y% länger)")
            upper_case = st.slider("Obere Grenze (Case)", 0.5, 1.0,upper_case, 0.01,help="Der Anzahl von Case-Dauer, der die Dauern so teilt, dass y% der Dauern kürzer oder gleich diesem Wert treiben(und x% länger)")
            factor_case = st.slider("Faktor (Case)", 1.0, 5.0, factor_case, 0.1,help="Ein häufig verwendeter Faktor (meist 1,5), um Ausreißer zu identifizieren")
            st.session_state['lower_case'] = lower_case
            st.session_state['upper_case'] = upper_case
            st.session_state['factor_case'] = factor_case


    outliers = outlier_trace(log_df)
    case_duration_df = duration_pro_case(log_df)
    # activity duration
    activity_df = duration_pro_activity(log_df)

    for category, indices in outliers.items():
        # if category in OUTLIER_DESCRIPTIONS:
        st.caption(OUTLIER_DESCRIPTIONS[category]["description"])

        with st.expander(f"### Kategorie: {category} | Anzahl Cases: {len(set(log_df.loc[indices, 'case_id']))}"):
            if indices:
                outlier_df = log_df.loc[indices]
            else:
                st.write("Keine Ausreißer in dieser Kategorie gefunden.")
                continue
            
            outlier_df=outlier_df.merge(
                    case_duration_df[["case_id","case_duration"]]  ,
                    on=["case_id"],
                    how="left"
                )
            outlier_df=outlier_df.merge(
                activity_df[
                        ["case_id", "timestamp","Activity_Duration_time"]
                    ],
                    on=["case_id","timestamp"],
                    how="left"   
            )                  
            for case_id, case_df in outlier_df.groupby("case_id"):
                _render_single_trace(category, case_id, case_df)