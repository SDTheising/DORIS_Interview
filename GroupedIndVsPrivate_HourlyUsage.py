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

# Individual Workstations
wk = (
    df.filter(pl.col("Type_clean") == "Individual Workstation")
      .group_by("hour")
      .agg((pl.col("occupied").mean() * 100).round(2).alias("wk_occupied"))
      .sort("hour")
)

# Private Offices
po = (
    df.filter(pl.col("Type_clean") == "Private Office")
      .group_by("hour")
      .agg((pl.col("occupied").mean() * 100).round(2).alias("po_occupied"))
      .sort("hour")
)

# Join on matching hour (assumes same workday coverage)
both = wk.join(po, on="hour", how="inner") 

# Extract for plotting
hours = both["hour"].to_list()
wk_values = both["wk_occupied"].to_list()
po_values = both["po_occupied"].to_list()

# Plot grouped bar chart
bar_width = 0.4
x = np.arange(len(hours))

plt.figure(figsize=(14, 6))
plt.bar(x - bar_width/2, wk_values, width=bar_width, label="Workstations")
plt.bar(x + bar_width/2, po_values, width=bar_width, label="Private Offices")

plt.xticks(x, hours)
plt.xlabel("Hour of Day")
plt.ylabel("% Occupied")
plt.title("Hourly Occupancy Rate: Workstations vs Private Offices")
plt.legend()
plt.tight_layout()
plt.savefig("./visuals/dual_occ_comparison.png", dpi=300)
plt.show()
