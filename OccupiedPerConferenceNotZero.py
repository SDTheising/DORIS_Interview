import polars as pl
import matplotlib.pyplot as plt

df = pl.read_excel("./DorisInt.xlsx")

# Load data.
df = pl.read_excel("./DorisInt.xlsx").with_columns([
    pl.col("Type").str.strip_chars().alias("Type_clean"),
    (pl.col("Status") == "Occupied").alias("occupied"),
    pl.col("Time").str.strptime(pl.Time, "%H:%M", strict=False).alias("ts")
]).with_columns(
    pl.col("ts").dt.hour().alias("hour")
)

pct_by_room = (
    df.filter(pl.col("Type_clean") == "Conference Room")
    .filter(pl.col("Occupancy") > 0)
    .group_by("Point", "ts")
    .agg(
        (pl.col("Occupancy").mean() * 1)
        .alias("num_occupants")
    ).sort("ts")
)

print(pct_by_room)


sizes = pct_by_room["num_occupants"].to_list()
labels = pct_by_room["Point"].to_list()

plt.figure()         
plt.bar(
    labels,
    height=sizes
)
plt.ylabel("Num Occupants")
plt.title("Average Occupancy (Excluding 0)")

plt.savefig("./visuals/num_occ_avg_conf.png", dpi=300)
plt.show()
