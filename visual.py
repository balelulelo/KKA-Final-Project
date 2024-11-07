# File to visualize the Shinkansesn route graph

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
    "Shinagawa": (0, 2.5),
    "Shin-Yokohama": (-0.5, 2),
    "Odawara": (-1, 1.5),
    "Atami": (-1.5, 1.5),
    "Mishima": (-2, 1.5),
    "Shin-Fuji": (-2.5, 1.5),
    "Shizuoka": (-3, 1.5),
    "Kakegawa": (-3.5, 1.5),
    "Hamamatsu": (-4, 1.5),
    "Toyohashi": (-4.5, 1.5),
    "Mikawa-Anjo": (-5, 1.5),
    "Nagoya": (-5.5, 1.5),
    "Gifu-Hashima": (-6, 1.5),
    "Maibara": (-6.5, 1.5),
    "Kyoto": (-7, 1.5),
    "Shin-Osaka": (-7.5, 1.5),
    
    # Tohoku Shinkansen (Northward from Tokyo)
    "Ueno": (0, 3.5),
    "Omiya": (0, 4),
    "Oyama": (0, 4.5),
    "Utsunomiya": (0, 5),
    "Nasu-Shiobara": (0, 5.5),
    "Shin-Shirakawa": (0, 6),
    "Koriyama": (0, 6.5),
    "Fukushima": (0, 7),
    "Sendai": (0, 7.5),
    "Furukawa": (0, 8),
    "Kurikoma-Kogen": (0, 8.5),
    "Ichinoseki": (0, 9),
    "Mizusawa-Esashi": (0, 9.5),
    "Kitakami": (0, 10),
    "Shin-Hanamaki": (0, 10.5),
    "Morioka":(0, 11),
    "Iwate-Numakunai": (0, 11.5),
    "Ninohe": (0, 12),
    "Hachinohe": (-0.5, 12),
    "Shichinohe-Towada": (-1, 12.5),
    "Shin-Aomori": (-1.5, 15),
    "Shizukuishi": (-1, 10),
    "Tazawako": (-1.5, 10),
    "Kakunodate": (-2, 10),
    "Omagari": (-2.5, 10),
    "Akita": (-3, 10),
    "Yonezawa": (-2, 6.5),
    "Takahata": (-2.5, 7),
    "Kaminayama": (-3, 8),
    "Yamagata": (-3.5, 8.5),
    "Tendo": (-3.5, 9),
    "Sakurambo": (-3.5, 9.5),
    "Murayama": (-3.5, 10),
    "Oishida": (-3.5, 10.5),
    "Shinjo": (-3.5, 11),
    
    # Hokuriku Shinkansen (from Tokyo towards northwest)
    "Annaka-Haruna": (-4.5, 5.5),
    "Karuizawa": (-5, 5.5),
    "Sakudaira": (-5.5, 5.5),
    "Ueda": (-6, 5.5),
    "Nagano": (-6.5, 6),
    "Joetsu-Myoko": (-6.5, 6.5),
    "Itoigawa": (-7, 6.5),
    "Kurobe-Unazukionsen": (-7.5, 6.5),
    "Toyama": (-8, 6.5),
    "Shin-Takaoka": (-8.5, 7),
    "Kanazawa": (-9, 6.5),
    "Fukui": (-9, 6),
    "Tsurugi": (-9, 5.5),
    
    # Joetsu Shinkansen (branching northwest from Omiya)
    "Kumagaya": (-4, 4),
    "Honjo-Waseda": (-4 , 4.5),
    "Takasaki": (-4, 5),
    "Jomo-Kogen": (-4, 5.5),
    "Echigo-Yuzawa": (-4, 6),
    "Gala-Yuzawa": (-4.5, 6.5),
    "Urasa": (-4, 6.5),
    "Nagaoka": (-4, 7),
    "Tsubame-Sanjo": (-4, 7.5),
    "Niigata": (-4, 9),
}


# Update the pos parameter in the drawing functions
plt.figure(figsize=(15, 10))

# Use custom positions if available; fallback to spring_layout for others
pos = {node: custom_positions.get(node, pos) for node, pos in nx.spring_layout(G, seed=42).items()}

# Draw nodes and edges using the custom positions
nx.draw_networkx_nodes(G, pos, node_size=200, node_color="skyblue")
nx.draw_networkx_edges(G, pos, arrowstyle="->", arrowsize=10, edge_color="gray", width=1)
nx.draw_networkx_labels(G, pos, font_size=8, font_family="sans-serif")

# Customizing edge labels
edge_labels = {(u, v): f"{d['line']} ({d['duration']} min)" for u, v, d in G.edges(data=True)}
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=6)

# Display the plot
plt.title("Shinkansen Routes Visualization")
plt.show()
