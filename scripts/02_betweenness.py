import osmnx as ox
import networkx as nx
import pandas as pd

G = ox.load_graphml(filepath="data/lagos_network.graphml")

print(f"Nodes: {len(G.nodes)}")
print(f"Edges: {len(G.edges)}")

# Calculate edge betweenness centrality
edge_centrality = nx.edge_betweenness_centrality(G, k=100, normalized=True) 

# k is the number of samples to use for approximation. Setting it to 100 means we will sample 100 nodes to estimate the betweenness centrality, which can speed up the calculation for large graphs.
# normalized=True is an instruction to NetworkX — it means "express centrality scores as a fraction between 0 and 1 instead of raw counts."

# Convert the edge centrality dictionary to a DataFrame for better visualization
df = pd.DataFrame([(u, v, centrality) for (u, v, key), centrality in edge_centrality.items()],
                   columns=['u', 'v', 'betweenness'])

# Sort by highest betweenness first
df = df.sort_values('betweenness', ascending=False)

print(df.head(10))

