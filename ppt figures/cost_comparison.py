import matplotlib.pyplot as plt

# Data for comparative cost chart
interventions = [
    "Mass Cleric Deployment",
    "21 Healing Potions",
    "One Suit of Plate Armor",
    "Elite Adventurer Team",
    "Magic Gear + Resurrections + Damages"
]

costs = [
    1081,   # Mass Cleric Deployment
    1050,   # 21 Healing Potions (50 gp each)
    1500,   # Plate Armor
    50000,  # Elite Adventurer Team
    75000   # Additional high-level intervention costs
]

# Create the bar chart
fig, ax = plt.subplots(figsize=(10, 6))
bars = ax.barh(interventions, costs, color=['#7fbf7f', '#c2c2f0', '#bfbfbf', '#ff9999', '#cc6666'])

# Annotate each bar with cost
for bar in bars:
    width = bar.get_width()
    ax.text(width + 500, bar.get_y() + bar.get_height()/2,
            f"{int(width):,} gp", va='center', fontsize=10)

# Chart aesthetics
ax.set_title("Comparative Costs of Tarrasque Response Strategies", fontsize=14, weight='bold')
ax.set_xlabel("Estimated Gold Cost")
ax.set_xlim(0, 80000)
ax.grid(axis='x', linestyle='--', alpha=0.5)

plt.tight_layout()
plt.savefig("cost_comparison.png")  # Save the figure
