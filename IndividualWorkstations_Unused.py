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

ws = df.filter(pl.col("Type_clean") == "Individual Workstation")



# For each workstation (Point), did it ever see occupancy?
used_per_ws = ws.group_by("Point").agg(
    pl.col("occupied").any().alias("used")
)

# Count number of used and unused stations
num_used = used_per_ws.filter(pl.col("used") == True).height
num_unused = used_per_ws.filter(pl.col("used") == False).height

print(num_used)
print(num_unused + num_used)

# Compute the two floats: % used vs % never used
pct_used  = used_per_ws.select((pl.col("used").mean() * 100).round(2)).to_series()[0]
pct_never = 100.0 - pct_used

# Plot the pie chart
sizes = [pct_used, pct_never]
labels = ["Used", "Never Used"]

plt.figure()
plt.pie(
    sizes,
    labels=labels,
    autopct="%1.1f%%",
    startangle=90,
    counterclock=False
)
plt.title("Workstations: % Used vs Never Used (Daily)")
plt.tight_layout()

plt.savefig("./visuals/pct_wk_stations_used.png", dpi=300)
plt.show()
