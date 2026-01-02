import streamlit as st
import pandas as pd
from io import StringIO
from Datenanalyse_Outlier.statistic_analysis.second_to_time import second_to_time
from Datenanalyse_Outlier.display_analysis.outlier_trace import create_trace_graph
from Datenanalyse_Outlier.statistic_analysis import temporal_outliers
from streamlit_elements import elements, nivo, mui
import re
from Datenanalyse_Outlier.map_columns import map_column

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

# für die Anzeige der case_id in der Graphik, funktioniert aber noch nicht so richtig
# df = map_column(df.copy())    

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
if len(resource_outliers)>0:
    _,grouped_resource_outliers= grouped_outliers(resource_outliers, has_type=False)

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
grouped_resource_outliers = st.session_state.get("resource_outliers_accepted",[])
for category, df_all in grouped_resource_outliers:
    resource= df_all["resource"].iloc[0]
    # category=i[0]
    st.write("---")
    st.subheader(f"Akzeptierte Ressourcen Ausreißer - {category}")
    for resource, res_df in df_all.groupby("resource"):
        # comment = i[1]["Kommentar"].iloc[0] if "Kommentar" in i[1].columns else ""
        # Resource fragment
        with st.expander(f"Ressource: {resource} | Anzahl Activities: {len(res_df)}", expanded=False):
            # Tabelle: alle Events dieser Resource
            st.dataframe(
                res_df[["case_id", "activity", "timestamp"]],hide_index=True,width="stretch",key = f"df_{category}_{resource}")
            # Barchart: Aktivitätsverteilung
            activity_counts = res_df.groupby("activity").size().reset_index(name="count")
            st.caption("📊 Aktivitätsverteilung dieser Ressource")
            st.bar_chart(activity_counts.set_index("activity")["count"])            
            comment_and_download_section(res_df, category, "Ressource",resource)
    
# Konvertierung von der Zeit wegen Anzeigenproblemen 
def duration_string_to_seconds(duration_str):
    if not isinstance(duration_str, str):
        return None
    pattern = r'(?:(\d+)mo)?\s*(?:(\d+)d)?\s*(?:(\d+)h)?\s*(?:(\d+)s)?'
    match = re.match(pattern, duration_str.strip())
    if not match:
        return None
    months, days, hours, seconds = match.groups(default="0")
    return int(months)*30*24*3600 + int(days)*24*3600 + int(hours)*3600 + int(seconds)

# Temporale Ausreißer: Button für Nivo-Chart
for category, data_df in grouped_temporal_outliers:
    st.write("---")
    # Anzeige Tabelle + Name Kategorie
    st.subheader(f"Akzeptierte Zeitliche Ausreißer - {category}")
    st.dataframe(data_df, width="stretch",hide_index=True,)
    # Kommentar und Download
    comment_and_download_section(data_df, category, "Zeitlich")

    chart_key = f"show_chart_{category}"
    if chart_key not in st.session_state: 
        st.session_state[chart_key] = False
    
    if st.button(f"📊 Zeitliche Ausreißer visualisieren ({category})", key=f"chart_btn_{category}"):
        st.session_state[chart_key] = not st.session_state[chart_key]
    if st.session_state[chart_key]:
        scatter_data = []
        
        for _, row in data_df.iterrows():
            # 1. Zeitstempel (X-Achse)
            ts = row.get("timestamp")
            
            # 2. Dauer (Y-Achse) - Wir nehmen die Spalte aus deinem Beispiel
            dur_raw = row.get("standard_activity_duration")
            
            if pd.isna(ts) or dur_raw is None or dur_raw == "-":
                continue
                
            try:
                # X-Achse konvertieren
                ts_dt = pd.to_datetime(ts)
                ts_iso = ts_dt.strftime("%Y-%m-%dT%H:%M:%S")
                
                # Y-Achse konvertieren
                sec = 0
                if isinstance(dur_raw, str):
                    # Reinigung: Pandas mag 'min' nicht, es will 'm' oder 'mins'
                    clean_dur = dur_raw.replace("min", "m")
                    try:
                        sec = pd.to_timedelta(clean_dur).total_seconds()
                    except:
                        # Falls das auch scheitert, probieren wir deine Regex-Funktion
                        sec = duration_string_to_seconds(dur_raw) or 0
                else:
                    sec = float(dur_raw)
                
                # In Minuten umrechnen
                dur_sec = sec 
                
                if dur_sec > 0:
                    scatter_data.append({
                        "x": ts_iso, 
                        "y": round(float(dur_sec), 2)
                    })
            except:
                continue

        if scatter_data:
            safe_id = re.sub(r'\W+', '', category)
            with elements(f"scatter_elements_{safe_id}"):
                with mui.Box(sx={"height": 450, "width": "100%"}):
                    nivo.ScatterPlot(
                        data=[{"id": str(category), "data": scatter_data}],
                        xScale={"type": "time", "format": "%Y-%m-%dT%H:%M:%S", "useUTC": False},
                        xFormat="time:%Y-%m-%d %H:%M",
                        yScale={"type": "linear", "min": "auto", "max": "auto"},
                        margin={"top": 40, "right": 50, "bottom": 80, "left": 70},
                        useMesh=True,
                        colors={"scheme": "nivo"},
                        axisBottom={"format": "%d.%m.%y", "tickRotation": -45, "legend": "Zeitpunkt", "legendOffset": 60},
                        axisLeft={"legend": "Dauer (sec)", "legendOffset": -60}
                    )
        else:
            st.info("Keine validen Daten zur Visualisierung gefunden. Prüfe, ob die Dauer-Spalte Werte enthält.")