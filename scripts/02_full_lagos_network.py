import osmnx as ox
import networkx as nx
import pandas as pd

# Step 1: Download full Lagos network
print ("Downloading full Lagos network... this may take a few minutes")
place = "Lagos, Nigeria"
G = ox.graph_from_place(place, network_type="drive")
print(f"Download complete. Nodes: {len(G.nodes)}, Edges: {len(G.edges)}")

# Step 2: Save it immediately
ox.save_graphml (G, filepath="data/lagos_full_network.graphml")
print("Network saved.")

# Step 3: Load from saved file
G = ox.load_graphml(filepath="data/lagos_full_network.graphml")
print("Network loaded from file.")

# Step 4: Approximate betweenness centrality using k samples
print("Calculating betweenness centrality (k=500)...")
centrality = nx.betweenness_centrality(G, k=500, normalized=True, weight="length")
print("Centrality calculation complete.")

# Step 5: Convert to DataFrame for visualization
df = pd.DataFrame([
    {"node_id": node, "betweenness_centrality": score}
    for node, score in centrality.items()
])

df = df.sort_values("betweenness_centrality", ascending=False)

# Step 6: Save results 
df.to_csv("outputs/lagos_full_centrality.csv", index=False)
print("Results saved to outputs/lagos_full_centrality.csv")
print(df.head(10))



# A dictionary has keys (the node IDs) and values (the scores). 
# .items() simply says "give me both sides at once, as pairs."

# So centrality.items() returns:
# (112453, 0.00847)
# (112454, 0.00012)
# ...

# Instead of; 
# centrality = {
#    112453: 0.00847,
#    112454: 0.00012,
# }
# It gives it something that opens in Excel.

# Now Step 5 makes full sense as one story:
# .items() — unpack every key-value pair from the dictionary
# {"node_id": node, "betweenness_centrality": score} — turn each pair into a labelled row
# pd.DataFrame([...]) — stack all those rows into a table
# .sort_values(...) — arrange the table highest centrality first (it reorders the rows from highest to lowest)


