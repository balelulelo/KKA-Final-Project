import pandas as pd
import heapq
from collections import deque, defaultdict
import time

start_time = time.time()
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
def timed_search(search_function, *args):
    start_time = time.time()
    result = search_function(*args)
    end_time = time.time()
    elapsed_time = end_time - start_time
    return result, elapsed_time

# Define function to find the best route based on selected criteria
def find_best_route(routes, criteria):
    selected_routes = []
    
    # Calculate and store route metrics based on the user's criteria
    for route in routes:
        if route[0]:  # Ensure the route exists
            path, lines, distance, cost, duration, transits = route
            score = []
            if 'fastest' in criteria:
                score.append(duration)
            if 'least_transit' in criteria:
                score.append(transits)
            if 'cheapest' in criteria:
                score.append(cost)
            median_score = sorted(score)[len(score) // 2]  # Get the median score
            selected_routes.append((path, lines, distance, cost, duration, transits, median_score))
    
    # Find the route with the best (lowest) median score
    best_route = min(selected_routes, key=lambda x: x[-1], default=None)
    return best_route
# Calculate combined score for each route based on a simple weighted metric
def calculate_combined_score(distance, cost, duration, transits, w_dist=0.25, w_cost=0.25, w_dur=0.25, w_trans=0.25):
    return (w_dist * distance) + (w_cost * cost) + (w_dur * duration) + (w_trans * transits)

# Find the ideal route based on combined score
def find_ideal_route(routes):
    best_route = None
    best_score = float('inf')
    for route in routes:
        if route[0]:  # Only consider found routes
            path, lines, distance, cost, duration, transits = route
            score = calculate_combined_score(distance, cost, duration, transits)
            if score < best_score:
                best_score = score
                best_route = (path, lines, distance, cost, duration, transits)
    return best_route, best_score

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
def dijkstra_search(graph, start, goal):
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
                    heuristic = 0 # Distance as heuristic
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
# Prompt user for travel preferences
print("\nPlease select your travel preferences (choose one or more options):")
print("1. Are you in a rush? (Fastest route)")
print("2. Are you carrying heavy items or feeling tired? (Least transit route)")
print("3. Are you on a budget? (Cheapest route)")
choices = input("Enter numbers separated by commas (e.g., 1,2 for fastest and least transit): ")
selected_criteria = set()

if '1' in choices:
    selected_criteria.add('fastest')
if '2' in choices:
    selected_criteria.add('least_transit')
if '3' in choices:
    selected_criteria.add('cheapest')

# Check for valid criteria selection
if not selected_criteria:
    print("No valid selection made. Please restart and choose at least one option.")
    exit()

# Run each search with timing
print("\nCalculating routes based on your preferences...\n")



# ------------------------------------------------------------------------------------
#                                       RESULT
# ------------------------------------------------------------------------------------

# Call every search method (Best, BFS, A*)
(best_path, best_lines, best_dist, best_cost, best_dur, best_transits), best_time = timed_search(best_first_search, graph, start_station, goal_station)
(bfs_path, bfs_lines, bfs_dist, bfs_cost, bfs_dur, bfs_transits), bfs_time = timed_search(bfs, graph, start_station, goal_station)
(dijkstra_path, dijkstra_lines, dijkstra_dist, dijkstra_cost, dijkstra_dur, dijkstra_transits), dijkstra_time = timed_search(dijkstra_search, graph, start_station, goal_station)
(transits_path, transits_lines, transits_transits), transits_time = timed_search(least_transits_search, graph, start_station, goal_station)
routes = [
    (best_path, best_lines, best_dist, best_cost, best_dur, best_transits),
    (bfs_path, bfs_lines, bfs_dist, bfs_cost, bfs_dur, bfs_transits),
    (dijkstra_path, dijkstra_lines, dijkstra_dist, dijkstra_cost, dijkstra_dur, dijkstra_transits),
]
# Calculate the ideal route
# Find the best route based on user's criteria
best_route = find_best_route(routes, selected_criteria)
# Display the ideal route for the customer
if best_route:
    path, lines, distance, cost, duration, transits, _ = best_route
    print("\nBest Route Based on Your Preferences:")
    print("Route:", " -> ".join(path))
    print("Lines:", " -> ".join(lines))
    print("Total Distance:", f"{distance:.2f}", "km")
    print("Total Cost:", f"{cost:.2f}", "Yen")
    print("Total Duration:", f"{duration:.2f}", "minutes")
    print("Total Transits:", transits)
else:
    print("No suitable route found based on your preferences.")

print("\nThank you for using our service")
print("We wish you a safe journey!")