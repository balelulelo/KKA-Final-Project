import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# Load CSV file
df = pd.read_csv("shinkansen.csv")

# Create a directed multi-graph
G = nx.MultiDiGraph()

# Add nodes and edges from the CSV file
for _, row in df.iterrows():
    source = row["Source_Stations"]
    destination = row["Destination_Stations"]
    line = row["Line"]
    distance = row["Distance_(Km)"]
    cost = row["Cost_(Yen)"]
    duration = row["Durations_(Min)"]
    
    # Add edge with attributes for each route
    G.add_edge(source, destination, line=line, distance=distance, cost=cost, duration=duration)

# Example of manually setting positions
custom_positions = {
    # Tokaido Shinkansen (East to West)
    "Tokyo": (0, 3),
    "Shinagawa": (0.5, 2.8),
    "Shin-Yokohama": (1, 2.5),
    "Odawara": (1.5, 2.3),
    "Atami": (2, 2.2),
    "Shizuoka": (2.5, 2.1),
    "Hamamatsu": (3, 2),
    "Toyohashi": (3.5, 1.9),
    "Nagoya": (4, 1.8),
    "Gifu-Hashima": (4.5, 1.7),
    "Maibara": (4.8, 1.6),
    "Kyoto": (5.5, 1.5),
    "Shin-Osaka": (6, 1.4),
    
    # Sanyo Shinkansen (continuing west from Shin-Osaka)
    "Shin-Kobe": (6.5, 1.3),
    "Nishi-Akashi": (7, 1.2),
    "Himeji": (7.5, 1.1),
    "Aioi": (7.8, 1.05),
    "Okayama": (8.5, 1),
    "Shin-Kurashiki": (9, 0.9),
    "Fukuyama": (9.5, 0.8),
    "Shin-Onomichi": (10, 0.7),
    "Mihara": (10.3, 0.65),
    "Higashi-Hiroshima": (10.8, 0.6),
    "Hiroshima": (11.5, 0.5),
    "Shin-Iwakuni": (12, 0.4),
    "Tokuyama": (12.5, 0.3),
    "Shin-Yamaguchi": (13, 0.2),
    "Asa": (13.5, 0.15),
    "Shin-Shimonoseki": (14, 0.1),
    "Kokura": (14.5, 0.05),
    "Hakata": (15, 0),
    
    # Tohoku Shinkansen (Northward from Tokyo)
    "Ueno": (0, 3.2),
    "Omiya": (0, 3.5),
    "Utsunomiya": (0, 3.8),
    "Koriyama": (0, 4.1),
    "Fukushima": (0, 4.3),
    "Sendai": (0, 4.6),
    "Shiroishi-Zao": (0.2, 4.4),
    "Ichinoseki": (0, 5),
    "Morioka": (0, 5.3),
    "Shin-Aomori": (0, 6),
    
    # Hokuriku Shinkansen (from Tokyo towards northwest)
    "Tokyo": (0, 3),
    "Ueno": (0.2, 3.2),
    "Omiya": (0.5, 3.4),
    "Takasaki": (1, 3.6),
    "Annaka-Haruna": (1.2, 3.7),
    "Karuizawa": (1.5, 3.8),
    "Sakudaira": (1.7, 3.9),
    "Ueda": (2, 4),
    "Nagano": (2.5, 4.1),
    "Itoigawa": (3, 4.3),
    "Toyama": (3.5, 4.5),
    "Kanazawa": (4, 4.6),
    "Fukui": (4.5, 4.5),
    
    # Joetsu Shinkansen (branching northwest from Omiya)
    "Omiya": (0, 3.5),  # shared with Tohoku
    "Kumagaya": (-0.5, 3.7),
    "Honjo-Waseda": (-1, 3.9),
    "Takasaki": (-1.5, 4.1),
    "Jomo-Kogen": (-2, 4.3),
    "Echigo-Yuzawa": (-2.5, 4.5),
    "Urasa": (-3, 4.6),
    "Nagaoka": (-3.5, 4.7),
    "Tsubame-Sanjo": (-4, 4.8),
    "Niigata": (-4.5, 5),
}


# Update the pos parameter in the drawing functions
plt.figure(figsize=(15, 10))

# Use custom positions if available; fallback to spring_layout for others
pos = {node: custom_positions.get(node, pos) for node, pos in nx.spring_layout(G, seed=42).items()}

# Draw nodes and edges using the custom positions
nx.draw_networkx_nodes(G, pos, node_size=50, node_color="skyblue")
nx.draw_networkx_edges(G, pos, arrowstyle="->", arrowsize=10, edge_color="gray", width=1)
nx.draw_networkx_labels(G, pos, font_size=8, font_family="sans-serif")

# Customizing edge labels
edge_labels = {(u, v): f"{d['line']} ({d['duration']} min)" for u, v, d in G.edges(data=True)}
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=6)

# Display the plot
plt.title("Shinkansen Routes Visualization")
plt.show()
