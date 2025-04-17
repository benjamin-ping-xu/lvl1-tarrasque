import matplotlib.pyplot as plt
import numpy as np

# Define labels for the saving throws and their values for the Tarrasque
labels = ['STR', 'DEX', 'CON', 'INT', 'WIS', 'CHA']
# Tarrasque's saving throw bonuses (as per official stat block)
stats = [10, 0, 10, 5, 7, 5]  # Only DEX is noticeably weak

# Radar chart setup
num_vars = len(labels)

# Repeat the first value to close the radar chart loop
stats += stats[:1]
angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
angles += angles[:1]

# Create the radar chart
fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
ax.plot(angles, stats, color='crimson', linewidth=2)
ax.fill(angles, stats, color='crimson', alpha=0.25)

# Customize the chart
ax.set_theta_offset(np.pi / 2)
ax.set_theta_direction(-1)
ax.set_thetagrids(np.degrees(angles[:-1]), labels)
ax.set_title("Tarrasque Saving Throw Profile", fontsize=16, weight='bold', y=1.1)
ax.set_ylim(0, 12)

# Annotate DEX as the weak point
dex_angle = angles[1]
dex_value = stats[1]
ax.annotate("Viable Save Target", 
            xy=(dex_angle, dex_value + 0.5), 
            xytext=(dex_angle, dex_value + 4),
            arrowprops=dict(arrowstyle="->", color="gray"),
            ha='center', color='dimgray', fontsize=10)

plt.tight_layout()
plt.savefig("tarrasque_saving_throws.png", dpi=300)
