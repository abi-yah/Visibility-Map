import pandas as pd
import osmnx as ox

# Step 1: Load enriahed centrality data
df = pd.read_csv("outputs/lagos_critical_nodes.csv")
print(f"Loaded {len(df)} nodes.") 

# Step 2: Add rank column
df["rank"] = df["betweenness_centrality"].rank(ascending=False).astype(int)
print("Rank column added.")

# Step 3: Assign criticality label
def assign_label(score):
    if score >= 0.1:
        return "High"
    elif score >=0.01:
        return "Medium"
    else: 
        return "Low"
    
df["criticality"] = df["betweenness_centrality"].apply(assign_label)
print("Criticality label assigned.")
print(df["criticality"].value_counts())

# Step 4: Get top 50 nodes for reverse geocoding
top50 = df.sort_values("rank").head(50).copy()
print("Reverse geocoding top 50 nodes...")

# Step 5: Reverse geocode to get street names
street_names = []
for _, row in top50.iterrows():
    try:
        location = ox.geocoder.reverse_geocode(row["latitude"], row["longitude"])
        street_names.append(location)
    except:
        street_names.append("Unknown")

top50["street_name"] = street_names
print("Reverse geocoding complete.")

# Step 5b: Add Google Maps links to top 50
top50["google_maps_link"] = top50.apply(
    lambda row: f"https://maps.google.com/?q={row['latitude']},{row['longitude']}", 
    axis=1
)

# Step 6: Save full dataset for John
df.to_csv("outputs/john_full_criticality.csv", index=False)
print("Full dataset saved to outputs/john_full_criticality.csv")

# Step 7: Save top 50 with street names
top50.to_csv("outputs/john_top50_critical_nodes.csv", index=False)
print("Top 50 saved to outputs/john_top50_criticality.csv")
print(top50[["rank", "street_name", "betweenness_centrality", "criticality"]].head(10))



# .sort_values() vs .rank()
# .sort_values() — reorders the rows from highest to lowest
# .rank() — adds a number to each row showing its position, but doesn't move anything

# Geocoding gives the coordinates, not the street names. Reverse geocoding does the opposite

# The inner [] is a Python list of column names:
# python["rank", "street_name", "betweenness_centrality", "criticality"]
# The outer [] is Pandas saying "select these columns from the DataFrame."
# So it's not one row — it's all rows, but only those 4 columns. You're trimming the table width, not the height.