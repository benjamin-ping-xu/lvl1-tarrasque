# Prepare a cleaned-up version of the code as a single block for user export

# Required libraries
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Create a fake timeline
years = list(range(1480, 1492))

# Generate fake baseline data
np.random.seed(42)
dragons = np.random.randint(300, 500, size=len(years))
undead = np.random.randint(200, 400, size=len(years))
demons = np.random.randint(100, 300, size=len(years))
tarrasque = [0, 5, 8, 12, 20, 35, 60, 120, 300, 600, 1500, 3200]

# Create DataFrame and normalize to death rate per 100,000
population = 10_000_000
scaling_factor = 100_000

df = pd.DataFrame({
    "Year (DR)": years,
    "Dragons": dragons,
    "Undead": undead,
    "Demons": demons,
    "Tarrasque": tarrasque[:len(years)]
})

df["Dragons_rate"] = (df["Dragons"] / population) * scaling_factor
df["Undead_rate"] = (df["Undead"] / population) * scaling_factor
df["Demons_rate"] = (df["Demons"] / population) * scaling_factor
df["Tarrasque_rate"] = (df["Tarrasque"] / population) * scaling_factor

# Manually adjust for historical event spikes
df.loc[df["Year (DR)"] == 1485, "Demons_rate"] += 6
df.loc[df["Year (DR)"] == 1486, "Demons_rate"] += 10
df.loc[df["Year (DR)"] == 1489, "Dragons_rate"] += 0
df.loc[df["Year (DR)"] == 1490, "Dragons_rate"] += 8
df.loc[df["Year (DR)"] == 1491, "Undead_rate"] += 7

# Plotting
plt.figure(figsize=(12, 7))
plt.plot(df["Year (DR)"], df["Dragons_rate"], label="Dragons", linewidth=2)
plt.plot(df["Year (DR)"], df["Undead_rate"], label="Undead", linewidth=2)
plt.plot(df["Year (DR)"], df["Demons_rate"], label="Demons", linewidth=2)
plt.plot(df["Year (DR)"], df["Tarrasque_rate"], label="Tarrasque", linewidth=2, linestyle='--')

# Add custom annotations
annotations = [
    (1485, "Rage of Demons", 2.5),
    (1486, "Demogorgon Surfaces", 4),
    (1489, "Cult of the Dragon Rises", 3),
    (1490, "Tiamat Nearly Returns", 6),
    (1491, "The Death Curse", 0)
]

for year, label, offset in annotations:
    y_value = df.loc[df["Year (DR)"] == year, ["Dragons_rate", "Undead_rate", "Demons_rate"]].max(axis=1).values[0]
    plt.annotate(label,
                 xy=(year, y_value),
                 xytext=(year + 0.2, y_value + offset),
                 arrowprops=dict(arrowstyle="->", color='gray'),
                 fontsize=10,
                 color='dimgray')

# Final presentation touches
plt.title("Faerûn Mortality Trends: Deaths per 100,000 by Major Threat", fontsize=14)
plt.xlabel("Year (Dalereckoning)", fontsize=12)
plt.ylabel("Deaths per 100,000 Inhabitants", fontsize=12)
plt.legend()
plt.grid(True)
plt.tight_layout()

# Save the figure
plt.savefig("mortality_trends.png", dpi=300)
