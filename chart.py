import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from PIL import Image

# Set Seaborn style for professional appearance
sns.set_style("whitegrid")
sns.set_context("talk")

# Generate realistic synthetic data for monthly revenue by segment
np.random.seed(42)

months = list(range(1, 13))
segments = ["Premium", "Standard", "Budget"]

rows = []
for year in [2024, 2025]:
    for segment in segments:
        base = {"Premium": 850_000, "Standard": 500_000, "Budget": 250_000}[segment]
        for month in months:
            # Seasonality: peaks around month 3 (spring) and 11–12 (festive)
            seasonal_factor = (
                1.0
                + 0.18 * np.sin((month - 3) / 12 * 2 * np.pi)  # spring bump
                + 0.22 * np.sin((month - 11) / 12 * 2 * np.pi)  # year-end bump
            )
            trend_factor = 1.00 + 0.04 * (year - 2024)  # 4% YoY growth
            noise = np.random.normal(loc=0.0, scale=0.04)  # ±4% variation
            revenue = base * seasonal_factor * trend_factor * (1 + noise)
            rows.append({
                "year": year,
                "month": month,
                "segment": segment,
                "monthly_revenue": max(revenue, 0),
            })

df = pd.DataFrame(rows)

# Create figure with exact size and DPI
fig = plt.figure(figsize=(8, 8), dpi=64)

# Create the lineplot
ax = sns.lineplot(
    data=df,
    x="month",
    y="monthly_revenue",
    hue="segment",
    style="year",
    markers=True,
    dashes=False,
    palette="deep",
)

# Set titles and labels
ax.set_title(
    "Monthly Revenue Trend by Customer Segment\nHeller Group – Executive Overview",
    fontsize=18,
    pad=16,
)
ax.set_xlabel("Month", fontsize=14)
ax.set_ylabel("Monthly Revenue (USD)", fontsize=14)
ax.legend(title="Segment · Year", loc="upper left", frameon=True)

# Save with exact pixel dimensions
plt.tight_layout()
plt.savefig("chart.png", dpi=64, bbox_inches=None, pad_inches=0)
plt.close()

# Optional: Verify image size
img = Image.open("chart.png")
print("Image size:", img.size)  # Should print (512, 512)
