
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Olympic History Analysis",
    page_icon="🏅",
    layout="wide"
)

# ---------- Styling ----------
st.markdown("""
<style>
.stApp {
    background-color: #0e1726;
    color: #ffffff;
}
h1, h2, h3 {
    color: #f5c542 !important;
}
[data-testid="stMetric"] {
    background-color: #19283d;
    padding: 16px;
    border-radius: 12px;
    border: 1px solid #34445b;
}
</style>
""", unsafe_allow_html=True)

st.title("🏅 Olympic History Analysis")
st.markdown("Explore Olympic participation, sports, and medal records from 1896 to 2016.")

# ---------- Load dataset ----------
@st.cache_data
def load_data():
    df = pd.read_csv("athlete_events.csv")
    return df

try:
    df = load_data()
except Exception as e:
    st.error(f"Could not load athlete_events.csv: {e}")
    st.stop()

required_columns = [
    "Year", "Season", "Team", "Name",
    "Sport", "Sex", "Medal", "Age"
]
missing = [col for col in required_columns if col not in df.columns]

if missing:
    st.error(f"Dataset is missing required columns: {', '.join(missing)}")
    st.stop()

# ---------- Sidebar filters ----------
st.sidebar.header("🔎 Dashboard Filters")

years = sorted(df["Year"].dropna().unique().astype(int).tolist())
if not years:
    st.error("No Olympic years were found in the dataset.")
    st.stop()

year_range = st.sidebar.slider(
    "Select Olympic year range",
    min_value=min(years),
    max_value=max(years),
    value=(min(years), max(years))
)

seasons = sorted(df["Season"].dropna().unique().tolist())
selected_seasons = st.sidebar.multiselect(
    "Select season",
    seasons,
    default=seasons
)

teams = sorted(df["Team"].dropna().unique().tolist())
selected_teams = st.sidebar.multiselect(
    "Select teams (optional)",
    teams
)

filtered_df = df[
    df["Year"].between(year_range[0], year_range[1])
].copy()

if selected_seasons:
    filtered_df = filtered_df[
        filtered_df["Season"].isin(selected_seasons)
    ]
else:
    filtered_df = filtered_df.iloc[0:0]

if selected_teams:
    filtered_df = filtered_df[
        filtered_df["Team"].isin(selected_teams)
    ]

if filtered_df.empty:
    st.warning("No records match the selected filters. Please change your filters.")
    st.stop()

# ---------- KPI cards ----------
medal_df = filtered_df[filtered_df["Medal"].notna()]
k1, k2, k3, k4 = st.columns(4)

k1.metric("Unique Athletes", f"{filtered_df['Name'].nunique():,}")
k2.metric("Teams", f"{filtered_df['NOC'].nunique():,}" if "NOC" in filtered_df.columns else f"{filtered_df['Team'].nunique():,}")
k3.metric("Sports", f"{filtered_df['Sport'].nunique():,}")
k4.metric("Medal Records", f"{len(medal_df):,}")

st.caption(
    "Counts reflect the selected filters. Medal records are athlete-event records, "
    "not necessarily unique physical medals."
)

# ---------- Medal distribution ----------
st.subheader("🥇 Medal Distribution")

medal_counts = (
    medal_df["Medal"]
    .value_counts()
    .reindex(["Gold", "Silver", "Bronze"], fill_value=0)
    .rename_axis("Medal")
    .reset_index(name="Records")
)

if medal_counts["Records"].sum() > 0:
    fig = px.pie(
        medal_counts,
        names="Medal",
        values="Records",
        title="Gold, Silver and Bronze Records",
        hole=0.35
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("No medal records match the selected filters.")

# ---------- Top teams ----------
st.subheader("🌍 Top 10 Teams by Medal Records")

if not medal_df.empty:
    top_teams = (
        medal_df.groupby("Team")
        .size()
        .reset_index(name="Medal Records")
        .sort_values("Medal Records", ascending=False)
        .head(10)
    )

    fig = px.bar(
        top_teams.sort_values("Medal Records"),
        x="Medal Records",
        y="Team",
        orientation="h",
        title="Top Teams",
        text="Medal Records"
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("No medal records available for this selection.")

# ---------- Participation trend ----------
st.subheader("📈 Olympic Participation Over Time")

participation = (
    filtered_df.groupby("Year")["Name"]
    .nunique()
    .reset_index(name="Unique Athletes")
)

fig = px.line(
    participation,
    x="Year",
    y="Unique Athletes",
    markers=True,
    title="Unique Athletes by Olympic Year"
)
st.plotly_chart(fig, use_container_width=True)

# ---------- Gender distribution ----------
st.subheader("👥 Participation by Gender")

gender_data = (
    filtered_df["Sex"]
    .map({"M": "Male", "F": "Female"})
    .fillna("Other/Unknown")
    .value_counts()
    .rename_axis("Gender")
    .reset_index(name="Entries")
)

fig = px.pie(
    gender_data,
    names="Gender",
    values="Entries",
    title="Athlete Entries by Gender",
    hole=0.35
)
st.plotly_chart(fig, use_container_width=True)

# ---------- Popular sports ----------
st.subheader("🏃 Most Popular Sports")

popular_sports = (
    filtered_df.groupby("Sport")
    .size()
    .reset_index(name="Athlete Entries")
    .sort_values("Athlete Entries", ascending=False)
    .head(10)
)

fig = px.bar(
    popular_sports.sort_values("Athlete Entries"),
    x="Athlete Entries",
    y="Sport",
    orientation="h",
    title="Top 10 Sports by Athlete Entries"
)
st.plotly_chart(fig, use_container_width=True)

# ---------- Age distribution ----------
st.subheader("🎂 Athlete Age Distribution")

age_data = filtered_df.dropna(subset=["Age"])

if not age_data.empty:
    fig = px.histogram(
        age_data,
        x="Age",
        nbins=25,
        title="Distribution of Athlete Ages"
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("Age data is unavailable for this selection.")

# ---------- NEW: Detailed medal tally ----------
st.subheader("🏅 Detailed Medal Tally")

if medal_df.empty:
    st.info("No medal records are available for the selected filters.")
else:
    medal_tally = (
        medal_df.groupby("Team")
        .agg(
            Gold=("Medal", lambda s: (s == "Gold").sum()),
            Silver=("Medal", lambda s: (s == "Silver").sum()),
            Bronze=("Medal", lambda s: (s == "Bronze").sum()),
            Total=("Medal", "count")
        )
        .reset_index()
        .sort_values("Total", ascending=False)
        .reset_index(drop=True)
    )

    st.dataframe(
        medal_tally,
        use_container_width=True,
        hide_index=True
    )

    st.download_button(
        label="📥 Download Medal Tally as CSV",
        data=medal_tally.to_csv(index=False).encode("utf-8"),
        file_name="olympic_medal_tally.csv",
        mime="text/csv"
    )

# ---------- Dataset preview ----------
st.subheader("📋 Filtered Dataset Preview")

st.dataframe(
    filtered_df.head(100),
    use_container_width=True,
    hide_index=True
)

st.caption(
    f"Showing up to 100 of {len(filtered_df):,} filtered rows."
)

st.markdown("---")
st.markdown(
    "Olympic History Analysis | Python • Pandas • Streamlit • Plotly"
)



st.markdown("---")

st.markdown(
    """
    <div style="text-align: center; padding: 20px;">
        <h3 style="color: #F2C14E;">Developed By</h3>
        <p style="font-size: 17px; color: white;">
            Priyanshi Verma &nbsp; | &nbsp; Sweli Mehta
        </p>
        <p style="font-size: 12px; color: #AAB4C3;">
            Olympic History Analysis · Python · Streamlit
        </p>
    </div>
    """,
    unsafe_allow_html=True
)
