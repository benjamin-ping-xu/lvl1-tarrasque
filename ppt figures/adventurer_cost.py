import matplotlib.pyplot as plt
import numpy as np

# Simulated data for demonstration
# Ego from 1 (humble) to 20 (legend in their own mind)
ego = np.linspace(1, 20)

# Exponentially increasing cost as ego rises
# Base cost might be 100 gp, scaling ridiculously
cost_gp = 100 * np.exp(0.35*ego) + 10

# Plotting the curve
plt.figure(figsize=(10, 6))
plt.plot(ego, cost_gp, color='darkred', linewidth=2)
plt.title("The Adventurer Dilemma: Gold Cost vs. Ego", fontsize=14)
plt.xlabel("Adventurer Ego (1 = Humble, 20 = Delusional)", fontsize=12)
plt.xticks(np.arange(1, 21, 1))
plt.ylabel("Cost to Hire (gp)", fontsize=12)
plt.grid(True)

# Annotate the absurdity
plt.annotate("Sustainable",
             xy=(1, 300),
             xytext=(1, 5000),
             arrowprops=dict(arrowstyle="->", color='green'),
             fontsize=10,
             color='green')

plt.annotate("Catastrophically Unsustainable",
             xy=(16, cost_gp[-10]),
             xytext=(10, cost_gp[-10] * 1.5),
             arrowprops=dict(arrowstyle="->", color='firebrick'),
             fontsize=10,
             color='firebrick')

plt.tight_layout()
plt.savefig("adventurer_cost.png")
