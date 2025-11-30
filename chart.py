import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# 1. Global Seaborn style for professional look
sns.set_style("whitegrid")
sns.set_context("talk")  # larger text for presentations

# 2. Generate realistic synthetic seasonal revenue data
np.random.seed(42)

months = list(range(1, 13))  # 1–12
segments = ["Premium", "Standard", "Budget"]

rows = []
for year in [2024, 2025]:
    for segment in segments:
        base = {
            "Premium": 850_000,
            "Standard": 500_000,
            "Budget": 250_000,
        }[segment]

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

            rows.append(
                {
                    "year": year,
                    "month": month,
                    "segment": segment,
                    "monthly_revenue": max(revenue, 0),
                }
            )

df = pd.DataFrame(rows)

# 3. Create the lineplot: Monthly revenue trend by customer segment
plt.figure(figsize=(8, 8))  # 8 in × 8 in

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

# 4. Professional titles and labels
ax.set_title(
    "Monthly Revenue Trend by Customer Segment\nHeller Group – Executive Overview",
    fontsize=18,
    pad=16,
)
ax.set_xlabel("Month", fontsize=14)
ax.set_ylabel("Monthly Revenue (USD)", fontsize=14)

ax.legend(
    title="Segment · Year",
    loc="upper left",
    frameon=True,
)

# 5. Ensure 512×512 pixels: 8 in × 8 in at 64 dpi
plt.tight_layout()
plt.savefig("chart.png", dpi=64, bbox_inches="tight")
plt.close()
