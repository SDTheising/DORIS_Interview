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


occupied_pct = (
    df.filter(pl.col("Type_clean") == "Individual Workstation").select(
        (pl.col("occupied").mean() * 100).round(2)
        .alias("pct_occupied")
    )
)

print(occupied_pct)

occ = occupied_pct["pct_occupied"][0] 

sizes = [occ, 100 - occ]
labels = ["Occupied", "Unoccupied"]

plt.figure()             
plt.pie(
    sizes,
    labels=labels,
    autopct="%1.1f%%"    
)
plt.title("Time Occupied vs Unoccupied\n(Individual Workspace)")

plt.savefig("./visuals/time_occ_wk_stations.png", dpi=300)

plt.show()