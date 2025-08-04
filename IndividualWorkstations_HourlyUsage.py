import polars as pl
from matplotlib import pyplot as plt

# Load data.
df = pl.read_excel("./DorisInt.xlsx").with_columns([
    pl.col("Type").str.strip_chars().alias("Type_clean"),
    (pl.col("Status") == "Occupied").alias("occupied"),
    pl.col("Time").str.strptime(pl.Time, "%H:%M", strict=False).alias("ts")
]).with_columns(
    pl.col("ts").dt.hour().alias("hour")
)

# Filter to only Individual Workstations
df = df.filter(pl.col("Type_clean") == "Individual Workstation")

# Group by hour and calculate occupancy %
hourly_pct = (
    df.group_by("hour")
      .agg((pl.col("occupied").mean() * 100).round(2).alias("pct_occupied"))
      .sort("hour")
)

print(hourly_pct)


plt.figure(figsize=(10, 6))
plt.bar(hourly_pct["hour"], hourly_pct["pct_occupied"])
plt.xlabel("Hour of Day")
plt.ylabel("% of Workstations Occupied")
plt.title("Hourly Usage Rate of Individual Workstations")
plt.xticks(hourly_pct["hour"])
plt.tight_layout()
plt.savefig("./visuals/ind_wk_stations_hourly.png", dpi=300)
plt.show()
