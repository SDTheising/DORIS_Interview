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



pct_by_room = (
    df.filter(pl.col("Type_clean") == "Conference Room")
    .group_by("Point")
    .agg(
        (pl.col("occupied").mean() * 100).round(2)
        .alias("pct_occupied")
    )
)

print(pct_by_room)


sizes = pct_by_room["pct_occupied"].to_list()
labels = pct_by_room["Point"].to_list()

plt.figure()            
plt.bar(
    labels,
    height=sizes
)
plt.ylabel("% Occupied")
plt.title("Percent Time Occupied per Conference Room")

plt.savefig("./visuals/pct_time_occ_conf.png", dpi=300)
plt.show()
