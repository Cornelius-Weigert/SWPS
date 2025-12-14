import streamlit as st
import plotly.express as px

st.set_page_config(page_title="📊 Outlier Analyse", layout="wide")
st.title("📊 Outlier Analyse (Plotly)")

# Prüfen, ob Outlier-Daten existieren
if "outliers" not in st.session_state or not st.session_state["outliers"]:
    st.warning("⚠️ Keine Outlier-Daten gefunden. Bitte zuerst auf der Upload-Seite Eventlog analysieren.")
    st.stop()

# Alle Outlier-Typen aus Session State
outlier_types = list(st.session_state["outliers"].keys())

# Kategorie auswählen
selected_type = st.selectbox("Wähle den Outlier-Typ aus:", options=outlier_types)

# DataFrame für den ausgewählten Typ
df_for_plot = st.session_state["outliers"][selected_type]

# Prüfen, ob 'activity'-Spalte existiert
activity_col_candidates = ["activity", "Activity", "concept:name", "task", "event", "event_name"]
activity_col = next((c for c in df_for_plot.columns if c in activity_col_candidates), None)

if activity_col is None:
    st.warning(f"⚠️ Keine Aktivitätsspalte für '{selected_type}' gefunden.")
    st.stop()

# Multiselect für Aktivitäten
activities = df_for_plot[activity_col].unique()
selected_activities = st.multiselect(
    "Wähle Aktivitäten aus:",
    options=activities,
    default=activities
)

# Filtern
filtered_df = df_for_plot[df_for_plot[activity_col].isin(selected_activities)]

# Statistik: Anzahl Outlier pro Aktivität
if "is_outlier" not in filtered_df.columns:
    filtered_df["is_outlier"] = 0  # default, falls Spalte fehlt

stats = filtered_df.groupby(activity_col)["is_outlier"].sum().reset_index()

# Plotly Bar Chart
fig = px.bar(
    stats,
    x=activity_col,
    y="is_outlier",
    title=f"Outlier pro Aktivität: {selected_type}",
    text="is_outlier",
    labels={activity_col: "Aktivität", "is_outlier": "Anzahl Outlier"}
)
fig.update_traces(marker_color="indianred", textposition="outside")
fig.update_layout(yaxis=dict(dtick=1))

st.plotly_chart(fig, use_container_width=True)
