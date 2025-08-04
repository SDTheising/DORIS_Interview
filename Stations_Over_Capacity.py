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
# Filter out conference rooms.
df = df.filter(pl.col("Type_clean") != "Conference Room")

# Find which stations ever went over capacity.
stations_over = (
    df.filter(pl.col("Occupancy") > pl.col("Capacity"))
      .select("Point")
      .unique()
)

# Get all individual stations.
total_stations = df.select("Point").unique()


num_over = stations_over.height
num_total = total_stations.height

print(num_over)
print(num_total)

percent_over = round((num_over / num_total) * 100, 2)

sizes = [percent_over, 100 - percent_over]
labels = ["Went Over", "Stayed Under"]

plt.figure()             
plt.pie(
    sizes,
    labels=labels,
    autopct="%1.1f%%"    
)
plt.title("Percentage of Stations\nThat Went Over Capacity")

plt.savefig("./visuals/over_capacity.png", dpi=300)

plt.show()