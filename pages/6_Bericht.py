import streamlit as st
import pandas as pd
from io import StringIO
from Datenanalyse_Outlier.statistic_analysis.second_to_time import second_to_time
from Datenanalyse_Outlier.display_analysis.outlier_trace import create_trace_graph

def grouped_outliers(outliers,has_type=True):
    """
    Group outliers by category and concatenate their dataframes.
    Args:
        outliers: List of tuples [(category, df), ...]
    Returns:
        List of tuples [(category, combined_df), ...] with unique categories
    """
    if not outliers:
        return []
    grouped_temporal = {}
    grouped_resource = {}
    # for category, df, outlier_type in outliers:
    #     if outlier_type == "temporal":
    #         if category in grouped_temporal:
    #             grouped_temporal[category] = pd.concat([grouped_temporal[category], df], ignore_index=True)
    #         else:
    #             grouped_temporal[category] = df.copy()
    #     elif outlier_type == "resource":
    #         if category in grouped_resource:
    #             grouped_resource[category] = pd.concat([grouped_resource[category], df], ignore_index=True)
    #         else:
    #             grouped_resource[category] = df.copy()    
    # return list(grouped_temporal.items()), list(grouped_resource.items())
    for item in outliers:
        if has_type:
            category, df, outlier_type = item
        else:
            category, df = item
            outlier_type = "resource"

        if outlier_type == "temporal":
            if category in grouped_temporal:
                grouped_temporal[category] = pd.concat([grouped_temporal[category], df], ignore_index=True)
            else:
                grouped_temporal[category] = df.copy()
        elif outlier_type == "resource":
            if category in grouped_resource:
                grouped_resource[category] = pd.concat([grouped_resource[category], df], ignore_index=True)
            else:
                grouped_resource[category] = df.copy()

    return list(grouped_temporal.items()), list(grouped_resource.items())


def grouped_outliers_trace(outliers):
    """
    Group outliers by category and concatenate their dataframes.
    Args:
        outliers: List of tuples [(category, df), ...]
    Returns:
        List of tuples [(category, combined_df), ...] with unique categories
    """
    grouped = {}
    for category, df in outliers:
        if category in grouped:
            grouped[category] = pd.concat([grouped[category], df], ignore_index=True)
        else:
            grouped[category] = df.copy()
    return list(grouped.items())

def comment_and_download_section(df, category, outlier_type,resource=None):
    resource_str=f"_{resource}"if resource else ""
    # Kommentar Funktion zu jeder Kategorie
    comment = st.text_area(
        "Kommentar zu dieser Kategorie",
        value = st.session_state.get(f"comment_{outlier_type}_{category}",""),
        key = f"comment_{outlier_type}_{category}{resource_str}",
        height=100
        )
    # CSV für Kategorie inklusive Kommentar
    csv_buffer = StringIO()
    df_with_comment = df.copy()
    df_with_comment["Kommentar"] = comment
    df_with_comment.to_csv(csv_buffer, index=False)

    # Download Funktion mit Kommentarspalte
    st.download_button(
        label="Tabelle herunterladen",
        data=csv_buffer.getvalue(),
        file_name=f"bericht_{category}.csv",
        mime="text/csv",
        key=f"download_{outlier_type}_{category}{resource_str}"
        )

st.title("📑 Bericht - Ausreißeranalyse")

st.button("Bericht zurücksetzen", on_click=lambda: (st.session_state["outliers_accepted"].clear(), st.session_state["trace_outliers_accepted"].clear()))


# Sicherheitscheck für df (falls leer)
df = st.session_state.get("df")
if df is None:
    st.warning("Bitte zuerst Ausreißeranalyse durchführen!")
    st.stop()
    
# Sicherheitscheck für outliers (falls leer)
outliers = st.session_state.get("outliers_accepted",[])
trace_outliers = st.session_state.get("trace_outliers_accepted",[])
resource_outliers=st.session_state.get("resource_outliers_accepted",[])
grouped_trace_outliers = []
grouped_temporal_outliers = []
grouped_resource_outliers = []

if len(outliers) == 0 and len(trace_outliers) == 0 and len(resource_outliers)==0:
    st.info("Es wurden noch keine Ausreißer für den Bericht ausgewählt!")
    st.stop()
if len(outliers) > 0:
    grouped_temporal_outliers, grouped_resource_outliers = grouped_outliers(outliers)
if len(trace_outliers) > 0:
    grouped_trace_outliers = grouped_outliers_trace(trace_outliers)
# if len(resource_outliers)>0:
#     _,grouped_resource_outliers= grouped_outliers(resource_outliers, has_type=False)

# Anzeige der akzeptierten trace Ausreißer
for i in grouped_trace_outliers: # i[0] = category, i[1] = df
    category = i[0]
    st.write("---")
    st.subheader(f"Akzeptierte Trace Ausreißer - {category}")
    for case_id, case_df in i[1].groupby("case_id"):
        case_duration=second_to_time(case_df["case_duration"].iloc[0])
        comment = i[1]["Kommentar"].iloc[0] if "Kommentar" in i[1].columns else ""
        with st.expander(f"Trace von Case ID: {case_id} | Case_Dauer: {case_duration} | Kommentar: {comment}"):
            st.dataframe(case_df[
                    ["activity","resource","timestamp","Activity_Duration_time"]]
                , width="stretch",hide_index=True,key=f"df_trace_outliers_{case_id}_{category}_{i}")
            # Trace visualisieren, wenn ein Button geklickt wird
            trace_visualize_button = st.button("Trace visualisieren",key=f"visualize_trace_{case_id}_{category}")
            if trace_visualize_button:
                st.graphviz_chart(create_trace_graph(case_df))
    comment_and_download_section(i[1], category, "Trace")

# #Anzeige der akzeptierten Resource Ausreißer
# for i in grouped_resource_outliers:
#     category = i[0]
#     st.subheader(f"Akzeptierte Ressourcen Ausreißer - {category}")
#     st.dataframe(i[1], width="stretch",hide_index=True,)
#     comment_and_download_section(i[1], category, "Ressource")

# Anzeige der akzeptierten Resource Ausreißer 
resource_outliers = st.session_state.get("resource_outliers_accepted",{})
if resource_outliers:
    st.write("---")
    st.subheader(f"Akzeptierte Ressourcen Ausreißer")
    for category, df_all in resource_outliers.items():
        st.markdown(f"Kategotie:{category}")
        for resource, res_df in df_all.groupby("resource"):
            # Resource fragment
            with st.expander(f"Ressource: {resource} | Anzahl Activities: {len(res_df)}"):
                # Tabelle: alle Events dieser Resource
                st.dataframe(
                    res_df[["case_id", "activity", "timestamp"]],hide_index=True,width="stretch",key = f"df_{category}_{resource}")
                # Barchart: Aktivitätsverteilung
                activity_counts = res_df.groupby("activity").size().reset_index(name="count")
                st.caption("📊 Aktivitätsverteilung dieser Ressource")
                st.bar_chart(activity_counts.set_index("activity")["count"])            
        comment_and_download_section(df_all, category, outlier_type="Ressource")

# Anzeige der akzeptierten zeitlichen Ausreißer    
for i in grouped_temporal_outliers:
    st.write("---")
    category = i[0]
    st.subheader(f"Akzeptierte zeitliche Ausreißer - {category}")
    st.dataframe(i[1], width="stretch", hide_index=True,)
    comment_and_download_section(i[1], category, "Zeitlich")