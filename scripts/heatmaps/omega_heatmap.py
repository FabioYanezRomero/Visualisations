import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd

# Example data structure based on your heatmap
data = np.array([
    [0.80, 0.35, 0.09, 0.12, 0.03],
    [0.78, 0.35, 0.15, 0.14, 0.03],
    [0.81, 0.38, 0.10, 0.08, 0.03],
    [0.93, 0.16, 0.06, 0.06, 0.03],
    [0.45, 0.06, 0.06, 0.06, 0.03],
])

rows = [
    "Level 1-4",
    "Level 1-3",    
    "Level 1-2",
    "Level 1",
    "Before Train"
]
cols = ["Level 1", "Level 2", "Level 3", "Level 4", "Level 5"]

fig, ax = plt.subplots(figsize=(8,6))
sns.heatmap(
    data, annot=True, fmt=".2f", cmap="RdYlGn", linewidths=2,
    xticklabels=cols, yticklabels=rows, cbar_kws={'label': ''},
    ax=ax, vmin=0, vmax=1, annot_kws={'weight': 'bold'}
)
ax.set_title("Problem: Arithmetic GCD", fontweight='bold', fontsize=16, pad=15)
ax.set_xlabel("Complexity level of Test Problems", fontsize=12, fontweight='bold')
ax.set_ylabel("", fontweight='bold')
plt.yticks(rotation=0, fontweight='bold')
plt.xticks(fontweight='bold')
plt.tight_layout()
plt.savefig("omega_heatmap.png", dpi=300, bbox_inches='tight')
plt.show()
