import polars as pl
import matplotlib.pyplot as plt


# Load data.
df = pl.read_excel("./DorisInt.xlsx").with_columns([
    pl.col("Type").str.strip_chars().alias("Type_clean"),
    (pl.col("Status") == "Occupied").alias("occupied"),
    pl.col("Time").str.strptime(pl.Time, "%H:%M", strict=False).alias("ts")
]).with_columns(
    pl.col("ts").dt.hour().alias("hour")
)

# Find percentage of stations filled, aggregated by time.
pct_by_time = (
    df.group_by("ts")
    .agg(
        (pl.col("occupied").mean() * 100).round(2)
        .alias("pct_occupied")
    )
    .sort("ts")
)

print(pct_by_time)

# Turn "Time" to usable time stamps.
labels = [t.strftime("%H:%M") for t in pct_by_time["ts"].to_list()]
sizes = pct_by_time["pct_occupied"].to_list()

plt.figure()             
plt.bar(
    labels,
    height=sizes
)
plt.ylabel("% Occupied")
plt.title("Percent Occupied per Hour")
plt.savefig("./visuals/pct_occ_per_hr.png", dpi=300)
plt.show()