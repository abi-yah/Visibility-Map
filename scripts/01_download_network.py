import osmnx as ox
import matplotlib.pyplot as plt

# Download a small part of Lagos first (Lagos Island)
place = "Lagos Island, Lagos, Nigeria"
G = ox.graph_from_place(place, network_type="drive")

# How many nodes and edges did we get?
print(f"Nodes: {len(G.nodes)}")
print(f"Edges: {len(G.edges)}")

# Plot it
fig, ax = ox.plot_graph(G, figsize=(10, 10), 
                         node_size=5, 
                         edge_linewidth=0.5,
                         show=True)

ox.save_graphml(G, filepath="data/lagos_network.graphml")
