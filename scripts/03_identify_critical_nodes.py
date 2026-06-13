import osmnx as ox
import pandas as pd

#Load saved network
print("Loading network...")
G = ox.load_graphml(filepath="data/lagos_full_network.graphml")
print("Network loaded.")

# Step 2: Load centrality results
centrality_df = pd.read_csv ("outputs/lagos_full_centrality.csv")
print(f"Centrality data loaded. {len(centrality_df)} nodes.")

# Step 3: Extract node coordinates from graph
print("Extracting node coordinates...")
nodes_gdf = ox.graph_to_gdfs(G, nodes=True, edges=False)
nodes_gdf = nodes_gdf.reset_index()[["osmid", "x", "y"]]
nodes_gdf = nodes_gdf.rename(columns={"osmid": "node_id", "x": "longitude", "y": "latitude"})

# Step 4: Merge coordinates with centrality scores
print("Merging data...")
merged_df = centrality_df.merge(nodes_gdf, on="node_id", how="left")
print(f"Merge complete. {len(merged_df)} rows.")

# Step 5: Save enriched results
merged_df.to_csv("outputs/lagos_critical_nodes.csv", index=False)
print("Saved to outputs/lagos_critical_nodes.csv")
print(merged_df.head(10))

