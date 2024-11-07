# ------------------------------------------------------------------------------------
#                     ARTIFICIAL INTELLIGENCE CONCEPT (2024/2025)    
#                                  FINAL PROJECT                            
# ------------------------------------------------------------------------------------

# Group 1:

# 1. Muiz Surya Fata             5025231005
# 2. Alfa Radithya Fanany        5025231008
# 3. Muhammad Iqbal Shafarel     5025231080
# 4. Ali Ridho                   5025231162
# 5. Faiz Adli Nugraha           5025231174
# ------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------

import pandas as pd
import heapq
from collections import deque, defaultdict

# Load dataset
df = pd.read_csv('shinkansen.csv')


# ------------------------------------------------------------------------------------
#                                   CONSTRUCT GRAPH
# ------------------------------------------------------------------------------------

# Create a graph from the dataset
graph = defaultdict(list)
for _, row in df.iterrows():
    source = row['Source_Stations']
    destination = row['Destination_Stations']
    line = row['Line']
    distance = row['Distance_(Km)']
    cost = row['Cost_(Yen)']
    duration = row['Durations_(Min)']
    graph[source].append((destination, line, distance, cost, duration))
    graph[destination].append((source, line, distance, cost, duration))  # <-- If undirected

# ------------------------------------------------------------------------------------
#                               SEARCH ALGORITHM FUNCTIONS
# ------------------------------------------------------------------------------------

# Search the route using Best-First Search
def best_first_search(graph, start, goal):
    queue = [(0, start, [start], [], 0, 0, 0)]  # (heuristic distance, station, path, lines, total_distance, total_cost, total_duration)
    visited = set()
    while queue:
        _, current, path, lines, total_distance, total_cost, total_duration = heapq.heappop(queue)
        if current == goal:
            return path, lines, total_distance, total_cost, total_duration
        if current not in visited:
            visited.add(current)
            for neighbor, line, dist, cost, dur in graph[current]:
                if neighbor not in visited:
                    heapq.heappush(queue, (dist, neighbor, path + [neighbor], lines + [line], total_distance + dist, total_cost + cost, total_duration + dur))
    return None, None, None, None, None

# Search the route using Breadth-First Search
def bfs(graph, start, goal):
    queue = deque([(start, [start], [], 0, 0, 0)])  # (station, path, lines, total_distance, total_cost, total_duration)
    visited = set([start])
    while queue:
        current, path, lines, total_distance, total_cost, total_duration = queue.popleft()
        if current == goal:
            return path, lines, total_distance, total_cost, total_duration
        for neighbor, line, dist, cost, dur in graph[current]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor], lines + [line], total_distance + dist, total_cost + cost, total_duration + dur))
    return None, None, None, None, None

# Search the route using A* Search
def a_star_search(graph, start, goal):
    queue = [(0, start, [start], [], 0, 0, 0)]  # (heuristic distance, station, path, lines, total_distance, total_cost, total_duration)
    visited = set()
    while queue:
        _, current, path, lines, total_distance, total_cost, total_duration = heapq.heappop(queue)
        if current == goal:
            return path, lines, total_distance, total_cost, total_duration
        if current not in visited:
            visited.add(current)
            for neighbor, line, dist, cost, dur in graph[current]:
                if neighbor not in visited:
                    heuristic = dist  
                    # Distance acts as the Heuristic value
                    heapq.heappush(queue, (total_distance + heuristic, neighbor, path + [neighbor], lines + [line], total_distance + dist, total_cost + cost, total_duration + dur))
    return None, None, None, None, None

# ------------------------------------------------------------------------------------
#                                  INPUT FROM USERS 
# ------------------------------------------------------------------------------------

# Get input from user
print("\nWelcome to Shinkansen Route Planning Service! Please wait for a moment... \n")
start_station = input("Which station are you from ?: ")
goal_station = input("Which station you want to go to ?: ")
print("\nCalculating Route, Distance, Cost, and Duration... \n")

# ------------------------------------------------------------------------------------
#                                       RESULT
# ------------------------------------------------------------------------------------

# Call every search method (Best, BFS, A*)
path_best, lines_best, distance_best, cost_best, duration_best = best_first_search(graph, start_station, goal_station)
path_bfs, lines_bfs, distance_bfs, cost_bfs, duration_bfs = bfs(graph, start_station, goal_station)
path_a_star, lines_a_star, distance_a_star, cost_a_star, duration_a_star = a_star_search(graph, start_station, goal_station)

# Cetak hasil pencarian
print("\nResult of Best-First Search:")
if path_best:
    print("Route:", " -> ".join(path_best))
    print("Lines:", " -> ".join(lines_best))
    print("Total Distance:", f"{distance_best:.2f}", "km")
    print("Total Cost:", f"{cost_best:.2f}", "Yen")
    print("Total Duration:", f"{duration_best:.2f}", "minutes")
else:
    print("Route not found.")

print("\nResult of Breadth-First Search:")
if path_bfs:
    print("Route:", " -> ".join(path_bfs))
    print("Lines:", " -> ".join(lines_bfs))
    print("Total Distance:", f"{distance_bfs:.2f}", "km")
    print("Total Cost:", f"{cost_bfs:.2f}", "Yen")
    print("Total Duration:", f"{duration_bfs:.2f}", "minutes")
else:
    print("Route not found.")

print("\nResult of A* Search:")
if path_a_star:
    print("Route:", " -> ".join(path_a_star))
    print("Lines:", " -> ".join(lines_a_star))
    print("Total Distance:", f"{distance_a_star:.2f}", "km")
    print("Total Cost:", f"{cost_a_star:.2f}", "Yen")
    print("Total Duration:", f"{duration_a_star:.2f}", "minutes")
else:
    print("Route not found.")

print("\nThank you for using our service")
print("We wish you a safe journey!")


