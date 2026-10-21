import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("athlete_events.csv")

df["Medal"] = df["Medal"].fillna("No Medal")
medals = df[df["Medal"] != "No Medal"]

top_countries = medals.groupby("Team")["Medal"].count().sort_values(ascending=False).head(10)

plt.figure(figsize=(10, 6))
top_countries.plot(kind="bar")

plt.title("Top 10 Countries by Olympic Medal Records")
plt.xlabel("Country")
plt.ylabel("Number of Medal Records")
plt.xticks(rotation=45)
plt.tight_layout()

plt.show()