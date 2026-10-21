
import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Olympic History Analysis",
    page_icon="🏅",
    layout="wide"
)

# ---------------- CUSTOM DESIGN ----------------
st.markdown("""
<style>
.stApp {
    background-color: #0b1120;
    color: #f8fafc;
}
[data-testid="stSidebar"] {
    background-color: #111c30;
}
[data-testid="stMetric"] {
    background-color: #162238;
    padding: 18px;
    border-radius: 12px;
    border: 1px solid #293750;
}
h1, h2, h3 {
    color: #f5c451 !important;
}
</style>
""", unsafe_allow_html=True)

# ---------------- LOAD DATA ----------------
@st.cache_data
def load_data():
    data = pd.read_csv("athlete_events.csv")
    data["Medal"] = data["Medal"].fillna("No Medal")
    data["Age"] = pd.to_numeric(data["Age"], errors="coerce")
    data["Year"] = pd.to_numeric(data["Year"], errors="coerce")
    return data

try:
    df = load_data()
except FileNotFoundError:
    st.error(
        "Dataset not found. Keep athlete_events.csv "
        "in the same folder as app.py."
    )
    st.stop()

# ---------------- HEADER ----------------
st.title("🏅 Olympic History Analysis")
st.markdown(
    "### Exploring Olympic history through data visualization"
)
st.caption(
    "Explore athletes, countries, sports and medal records "
    "across the Olympic Games."
)

# ---------------- SIDEBAR FILTERS ----------------
st.sidebar.title("🔎 Dashboard Filters")

years = sorted(df["Year"].dropna().astype(int).unique())

year_range = st.sidebar.slider(
    "Select Olympic year range",
    min_value=int(min(years)),
    max_value=int(max(years)),
    value=(int(min(years)), int(max(years)))
)

seasons = sorted(df["Season"].dropna().unique())
selected_seasons = st.sidebar.multiselect(
    "Select season",
    seasons,
    default=seasons
)

countries = sorted(df["Team"].dropna().unique())
selected_countries = st.sidebar.multiselect(
    "Select countries (optional)",
    countries
)

# ---------------- FILTER DATA ----------------
filtered = df[
    df["Year"].between(year_range[0], year_range[1])
    & df["Season"].isin(selected_seasons)
].copy()

if selected_countries:
    filtered = filtered[
        filtered["Team"].isin(selected_countries)
    ]

if filtered.empty:
    st.warning("No records match these filters.")
    st.stop()

medals = filtered[filtered["Medal"] != "No Medal"].copy()

# ---------------- KPI CARDS ----------------
athletes = filtered["ID"].nunique()
country_count = filtered["NOC"].nunique()
sports_count = filtered["Sport"].nunique()
medal_records = len(medals)

c1, c2, c3, c4 = st.columns(4)

c1.metric("Unique Athletes", f"{athletes:,}")
c2.metric("Countries / NOCs", f"{country_count:,}")
c3.metric("Sports", f"{sports_count:,}")
c4.metric("Medal Records", f"{medal_records:,}")

st.divider()

# ---------------- MEDAL PIE CHART ----------------
left, right = st.columns(2)

with left:
    st.subheader("🥇 Medal Distribution")

    medal_counts = medals["Medal"].value_counts().reindex(
        ["Gold", "Silver", "Bronze"], fill_value=0
    ).reset_index()
    medal_counts.columns = ["Medal", "Count"]

    if medal_counts["Count"].sum() > 0:
        fig = px.pie(
            medal_counts,
            names="Medal",
            values="Count",
            hole=0.45,
            color="Medal",
            color_discrete_map={
                "Gold": "#f5c451",
                "Silver": "#cbd5e1",
                "Bronze": "#c47b45"
            }
        )
        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            font_color="white"
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No medal records for the selected filters.")

# ---------------- TOP COUNTRIES ----------------
with right:
    st.subheader("🌍 Top 10 Countries by Medals")

    country_medals = (
        medals.groupby("Team")
        .size()
        .sort_values(ascending=False)
        .head(10)
        .reset_index(name="Medal Records")
    )

    fig = px.bar(
        country_medals.sort_values("Medal Records"),
        x="Medal Records",
        y="Team",
        orientation="h",
        color="Medal Records",
        color_continuous_scale=["#64748b", "#f5c451"],
        labels={"Team": "Country / Team"}
    )
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        showlegend=False
    )
    st.plotly_chart(fig, use_container_width=True)

st.divider()

# ---------------- PARTICIPATION TREND ----------------
st.subheader("📈 Olympic Participation Over Time")

participation = (
    filtered.groupby("Year")["ID"]
    .nunique()
    .reset_index(name="Unique Athletes")
)

fig = px.line(
    participation,
    x="Year",
    y="Unique Athletes",
    markers=True,
    labels={"Year": "Olympic Year"}
)
fig.update_traces(line_color="#f5c451")
fig.update_layout(
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)"
)
st.plotly_chart(fig, use_container_width=True)

# ---------------- GENDER ANALYSIS ----------------
left, right = st.columns(2)

with left:
    st.subheader("👥 Athlete Entries by Gender")

    gender_data = (
        filtered["Sex"].map({"M": "Male", "F": "Female"})
        .fillna("Other / Unknown")
        .value_counts()
        .reset_index()
    )
    gender_data.columns = ["Gender", "Entries"]

    fig = px.pie(
        gender_data,
        names="Gender",
        values="Entries",
        hole=0.4,
        color_discrete_sequence=["#4ea5d9", "#f08bb4", "#a5b4fc"]
    )
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)"
    )
    st.plotly_chart(fig, use_container_width=True)

# ---------------- POPULAR SPORTS ----------------
with right:
    st.subheader("🏃 Most Popular Sports")

    sports = (
        filtered.groupby("Sport")["ID"]
        .count()
        .sort_values(ascending=False)
        .head(10)
        .sort_values()
        .reset_index(name="Athlete Entries")
    )

    fig = px.bar(
        sports,
        x="Athlete Entries",
        y="Sport",
        orientation="h",
        color="Athlete Entries",
        color_continuous_scale=["#64748b", "#38bdf8"]
    )
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        showlegend=False
    )
    st.plotly_chart(fig, use_container_width=True)

# ---------------- AGE ANALYSIS ----------------
st.divider()
st.subheader("🎯 Athlete Age Distribution")

age_data = filtered.dropna(subset=["Age"])

fig = px.histogram(
    age_data,
    x="Age",
    nbins=30,
    labels={"Age": "Age in Years"},
    color_discrete_sequence=["#f5c451"]
)
fig.update_layout(
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)"
)
st.plotly_chart(fig, use_container_width=True)

# ---------------- DATA PREVIEW ----------------
with st.expander("View dataset preview"):
    st.dataframe(filtered.head(100), use_container_width=True)

st.caption(
    "Olympic History Analysis | Data visualization project"
)
