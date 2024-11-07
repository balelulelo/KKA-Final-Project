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
def least_transits_search(graph, start, goal):
    queue = deque([(start, [start], [], 0)])  # (station, path, lines, transit_count)
    visited = set([(start, None)])  # Track visited stations with previous line to avoid redundant paths
    
    while queue:
        current, path, lines, transit_count = queue.popleft()
        
        if current == goal:
            return path, lines, transit_count  # Return path, distinct lines, and transit count
        
        for neighbor, line, _, _, _ in graph[current]:
            # Ensure we only visit each station with a specific line once
            if (neighbor, line) not in visited:
                visited.add((neighbor, line))
                new_lines = lines.copy()
                new_transit_count = transit_count
                
                # Only add the line if it's different from the previous line
                if not lines or lines[-1] != line:
                    new_lines.append(line)
                    new_transit_count += 1 if lines else 0  # Increment transit only if there's a previous line
                
                queue.append((neighbor, path + [neighbor], new_lines, new_transit_count))
    
    return None, None, None  # Return None if no route is found

# Search the route using Best-First Search with transit counting
def best_first_search(graph, start, goal):
    queue = [(0, start, [start], [], 0, 0, 0, 0)]  # (heuristic distance, station, path, lines, total_distance, total_cost, total_duration, transit_count)
    visited = set()
    while queue:
        _, current, path, lines, total_distance, total_cost, total_duration, transit_count = heapq.heappop(queue)
        if current == goal:
            return path, lines, total_distance, total_cost, total_duration, transit_count
        if current not in visited:
            visited.add(current)
            for neighbor, line, dist, cost, dur in graph[current]:
                if neighbor not in visited:
                    new_transit_count = transit_count
                    new_lines = lines.copy()
                    # Only add line if it's different from the previous line
                    if not lines or lines[-1] != line:
                        new_lines.append(line)
                        new_transit_count += 1 if lines else 0  # Count transit if there's a previous line
                    heapq.heappush(queue, (dist, neighbor, path + [neighbor], new_lines, total_distance + dist, total_cost + cost, total_duration + dur, new_transit_count))
    return None, None, None, None, None, None

# Search the route using Breadth-First Search with transit counting
def bfs(graph, start, goal):
    queue = deque([(start, [start], [], 0, 0, 0, 0)])  # (station, path, lines, total_distance, total_cost, total_duration, transit_count)
    visited = set([start])
    while queue:
        current, path, lines, total_distance, total_cost, total_duration, transit_count = queue.popleft()
        if current == goal:
            return path, lines, total_distance, total_cost, total_duration, transit_count
        for neighbor, line, dist, cost, dur in graph[current]:
            if neighbor not in visited:
                visited.add(neighbor)
                new_transit_count = transit_count
                new_lines = lines.copy()
                # Only add line if it's different from the previous line
                if not lines or lines[-1] != line:
                    new_lines.append(line)
                    new_transit_count += 1 if lines else 0  # Count transit if there's a previous line
                queue.append((neighbor, path + [neighbor], new_lines, total_distance + dist, total_cost + cost, total_duration + dur, new_transit_count))
    return None, None, None, None, None, None

# Search the route using A* Search with transit counting
def a_star_search(graph, start, goal):
    queue = [(0, start, [start], [], 0, 0, 0, 0)]  # (heuristic distance, station, path, lines, total_distance, total_cost, total_duration, transit_count)
    visited = set()
    while queue:
        _, current, path, lines, total_distance, total_cost, total_duration, transit_count = heapq.heappop(queue)
        if current == goal:
            return path, lines, total_distance, total_cost, total_duration, transit_count
        if current not in visited:
            visited.add(current)
            for neighbor, line, dist, cost, dur in graph[current]:
                if neighbor not in visited:
                    heuristic = dist  # Distance as heuristic
                    new_transit_count = transit_count
                    new_lines = lines.copy()
                    # Only add line if it's different from the previous line
                    if not lines or lines[-1] != line:
                        new_lines.append(line)
                        new_transit_count += 1 if lines else 0  # Count transit if there's a previous line
                    heapq.heappush(queue, (total_distance + heuristic, neighbor, path + [neighbor], new_lines, total_distance + dist, total_cost + cost, total_duration + dur, new_transit_count))
    return None, None, None, None, None, None

# ------------------------------------------------------------------------------------
#                                  INPUT FROM USERS 
# ------------------------------------------------------------------------------------

print("\nWelcome to Shinkansen Route Planning Service! Please wait for a moment... \n")
start_station = input("Which station are you from ?: ")
goal_station = input("Which station you want to go to ?: ")
print("\nCalculating Route, Distance, Cost, and Duration... \n")

# ------------------------------------------------------------------------------------
#                                       RESULT
# ------------------------------------------------------------------------------------

# Call every search method (Best, BFS, A*)
path_best, lines_best, distance_best, cost_best, duration_best, transits_best = best_first_search(graph, start_station, goal_station)
path_bfs, lines_bfs, distance_bfs, cost_bfs, duration_bfs, transits_bfs = bfs(graph, start_station, goal_station)
path_a_star, lines_a_star, distance_a_star, cost_a_star, duration_a_star, transits_a_star = a_star_search(graph, start_station, goal_station)
path_least_transits, lines_least_transits, transits_least_transits = least_transits_search(graph, start_station, goal_station)
# Display results for Best-First Search
print("\nResult of Best-First Search:")
if path_best:
    print("Route:", " -> ".join(path_best))
    print("Lines:", " -> ".join(lines_best))
    print("Total Distance:", f"{distance_best:.2f}", "km")
    print("Total Cost:", f"{cost_best:.2f}", "Yen")
    print("Total Duration:", f"{duration_best:.2f}", "minutes")
    print("Total Transits:", transits_best)
else:
    print("Route not found.")

# Display results for Breadth-First Search
print("\nResult of Breadth-First Search:")
if path_bfs:
    print("Route:", " -> ".join(path_bfs))
    print("Lines:", " -> ".join(lines_bfs))
    print("Total Distance:", f"{distance_bfs:.2f}", "km")
    print("Total Cost:", f"{cost_bfs:.2f}", "Yen")
    print("Total Duration:", f"{duration_bfs:.2f}", "minutes")
    print("Total Transits:", transits_bfs)
else:
    print("Route not found.")

# Display results for A* Search
print("\nResult of A* Search:")
if path_a_star:
    print("Route:", " -> ".join(path_a_star))
    print("Lines:", " -> ".join(lines_a_star))
    print("Total Distance:", f"{distance_a_star:.2f}", "km")
    print("Total Cost:", f"{cost_a_star:.2f}", "Yen")
    print("Total Duration:", f"{duration_a_star:.2f}", "minutes")
    print("Total Transits:", transits_a_star)
else:
    print("Route not found.")

print("\nResult with the Least amount of transits Search:")
if path_least_transits:
    print("Route:", " -> ".join(path_least_transits))
    print("Lines:", " -> ".join(lines_least_transits))
    print("Total Transits:", transits_least_transits)
else:
    print("Route not found.")

print("\nThank you for using our service")
print("We wish you a safe journey!")