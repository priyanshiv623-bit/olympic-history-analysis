# Olympic History Analysis 🏅

## 📌 Project Overview

**Olympic History Analysis** is a Python-based data analysis and interactive visualization project that explores Olympic Games history from **1896 to 2016**.

The project uses athlete and event data to explore participation trends, medal achievements, gender distribution, popular sports, and athlete demographics through an interactive dashboard.

## 👥 Team Members

- **Priyanshi Verma**
- **Sweli Mehta**

This is a collaborative academic project. Team responsibilities are divided across development, analysis, visualization, testing, and documentation.

## 🎯 Project Objectives

- Analyze Olympic participation over time.
- Identify countries and teams with the highest medal counts.
- Explore Gold, Silver, and Bronze medal distributions.
- Compare male and female athlete participation.
- Identify popular sports based on athlete-event records.
- Explore athlete age distributions.
- Present findings through clear, interactive visualizations.
- Make Olympic data easier to explore and understand.

## 📊 Dataset

**Dataset:** 120 Years of Olympic History — Athletes and Results

**Source:** Kaggle

**Coverage:** Olympic Games from 1896 to 2016.

The dataset contains information about athletes, teams, National Olympic Committees (NOCs), sports, events, Olympic years, seasons, gender, age, and medal results.

Place `athlete_events.csv` in the project root directory before running the dashboard.

## 📈 Dashboard Features

The interactive dashboard currently includes:

1. **Key Performance Indicators** — Unique athletes, NOCs, sports, and medal records.
2. **Medal Distribution** — Pie chart comparing Gold, Silver, and Bronze medal records.
3. **Top 10 Countries/Teams** — Bar chart ranking teams by medal records.
4. **Olympic Participation Trends** — Line chart showing unique athletes across Olympic years.
5. **Gender Analysis** — Pie chart comparing male and female athlete-event entries.
6. **Popular Sports** — Bar chart of sports with the most athlete-event records.
7. **Athlete Age Distribution** — Histogram showing the distribution of recorded athlete ages.
8. **Interactive Filters** — Filter results by Olympic year range, season, and selected teams.
9. **Dataset Preview** — Inspect a sample of the filtered records.

**Note:** Medal records, athlete-event entries, unique athletes, and unique NOCs are different measures. The charts use the relevant measure for each analysis.

## 🛠️ Technologies Used

- **Python** — Main programming language.
- **Pandas** — Data loading, cleaning, grouping, and analysis.
- **Streamlit** — Interactive dashboard interface.
- **Plotly** — Interactive charts and visualizations.
- **Git and GitHub** — Version control and collaboration.

## 📁 Project Structure

```text
olympic-history-analysis/
├── README.md
├── .gitignore
├── main.py
├── app.py
├── requirements.txt
└── athlete_events.csv
```

## 🚀 How to Run the Project

### 1. Clone the repository

```bash
git clone https://github.com/priyanshiv623-bit/olympic-history-analysis.git
cd olympic-history-analysis
```

### 2. Create a virtual environment (recommended)

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Install the required libraries

```bash
python -m pip install -r requirements.txt
```

### 4. Launch the dashboard

```bash
python -m streamlit run app.py
```

Streamlit will provide a local URL, usually `http://localhost:8501`, where the dashboard can be viewed.

## 🤝 Collaboration

The project is maintained by Priyanshi Verma and Sweli Mehta. Development tasks include dashboard implementation, data analysis, visualization, testing, and documentation.

Individual responsibilities and contributions should be documented according to the work completed by each team member.

## 📌 Project Status

The initial dashboard implementation is running locally. Further work may include validation of analytical results, improved insights, additional visualizations, interface refinements, and final documentation.

## 👩‍💻 Authors

**Priyanshi Verma & Sweli Mehta**

GitHub Repository: https://github.com/priyanshiv623-bit/olympic-history-analysis
