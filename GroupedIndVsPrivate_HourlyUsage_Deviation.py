import polars as pl
import matplotlib.pyplot as plt
import numpy as np

# Load data.
df = pl.read_excel("./DorisInt.xlsx").with_columns([
    pl.col("Type").str.strip_chars().alias("Type_clean"),
    (pl.col("Status") == "Occupied").alias("occupied"),
    pl.col("Time").str.strptime(pl.Time, "%H:%M", strict=False).alias("ts")
]).with_columns(
    pl.col("ts").dt.hour().alias("hour")
)

# Get hourly occupancy for each type.

wk = (
    df.filter(pl.col("Type_clean") == "Individual Workstation")
      .group_by("hour")
      .agg((pl.col("occupied").mean() * 100).round(2).alias("wk_occupied"))
      .sort("hour")
)

po = (
    df.filter(pl.col("Type_clean") == "Private Office")
      .group_by("hour")
      .agg((pl.col("occupied").mean() * 100).round(2).alias("po_occupied"))
      .sort("hour")
)

# Join by hour.
both = wk.join(po, on="hour")

# Compute mean and deviation per type.
wk_avg = both["wk_occupied"].mean()
po_avg = both["po_occupied"].mean()

both = both.with_columns([
    (pl.col("wk_occupied") - wk_avg).alias("wk_dev"),
    (pl.col("po_occupied") - po_avg).alias("po_dev")
])

# Extract for plotting.
hours = both["hour"].to_list()
wk_dev = both["wk_dev"].to_list()
po_dev = both["po_dev"].to_list()

# Plot deviation chart.
bar_width = 0.4
x = np.arange(len(hours))

plt.figure(figsize=(14, 6))
plt.bar(x - bar_width/2, wk_dev, width=bar_width, label="Workstations", color='steelblue')
plt.bar(x + bar_width/2, po_dev, width=bar_width, label="Private Offices", color='darkorange')

plt.axhline(0, color='black', linewidth=1)
plt.xticks(x, hours)
plt.xlabel("Hour of Day")
plt.ylabel("Deviation from Daily Average (% Occupied)")
plt.title("Hourly Occupancy Deviation: Workstations vs Private Offices")
plt.legend()
plt.tight_layout()
plt.savefig("./visuals/dual_occ_deviation.png", dpi=300)
plt.show()
