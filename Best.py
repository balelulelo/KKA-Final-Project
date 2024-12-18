import pandas as pd
import heapq
from collections import deque, defaultdict
import time

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
    graph[destination].append((source, line, distance, cost, duration))  # Undirected graph

# ------------------------------------------------------------------------------------
#                               SEARCH ALGORITHM FUNCTIONS
# ------------------------------------------------------------------------------------

def timed_search(search_function, *args):
    start_time = time.time()
    result = search_function(*args)
    end_time = time.time()
    elapsed_time = end_time - start_time
    return result, elapsed_time

# Function to rank and retrieve the best route based on a chosen criterion
def get_best_route(routes, criterion):
    best_route = None
    best_score = float('inf')
    
    # Evaluate routes based on the selected criterion
    for route in routes:
        if route[0]:  # Only consider valid routes
            path, lines, distance, cost, duration, transits = route
            if criterion == 'fastest':
                score = duration
            elif criterion == 'least_transit':
                score = transits
            elif criterion == 'cheapest':
                score = cost
            if score < best_score:
                best_route = (path, lines, distance, cost, duration, transits)
                best_score = score
    
    return best_route

# Route-finding algorithms
def least_transits_search(graph, start, goal):
    queue = deque([(start, [start], [], 0)])  # (station, path, lines, transit_count)
    visited = set([(start, None)])
    
    while queue:
        current, path, lines, transit_count = queue.popleft()
        
        if current == goal:
            return path, lines, 0, 0, 0, transit_count
        
        for neighbor, line, _, _, _ in graph[current]:
            if (neighbor, line) not in visited:
                visited.add((neighbor, line))
                new_lines = lines.copy()
                new_transit_count = transit_count
                
                if not lines or lines[-1] != line:
                    new_lines.append(line)
                    new_transit_count += 1 if lines else 0
                
                queue.append((neighbor, path + [neighbor], new_lines, new_transit_count))
    
    return None, None, None, None, None, None

def best_first_search(graph, start, goal):
    queue = [(0, start, [start], [], 0, 0, 0, 0)]
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
                    if not lines or lines[-1] != line:
                        new_lines.append(line)
                        new_transit_count += 1 if lines else 0
                    heapq.heappush(queue, (dist, neighbor, path + [neighbor], new_lines, total_distance + dist, total_cost + cost, total_duration + dur, new_transit_count))
    return None, None, None, None, None, None

def bfs(graph, start, goal):
    queue = deque([(start, [start], [], 0, 0, 0, 0)])
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
                if not lines or lines[-1] != line:
                    new_lines.append(line)
                    new_transit_count += 1 if lines else 0
                queue.append((neighbor, path + [neighbor], new_lines, total_distance + dist, total_cost + cost, total_duration + dur, new_transit_count))
    return None, None, None, None, None, None

def dijkstra_search(graph, start, goal):
    queue = [(0, start, [start], [], 0, 0, 0, 0)]
    visited = set()
    while queue:
        _, current, path, lines, total_distance, total_cost, total_duration, transit_count = heapq.heappop(queue)
        if current == goal:
            return path, lines, total_distance, total_cost, total_duration, transit_count
        if current not in visited:
            visited.add(current)
            for neighbor, line, dist, cost, dur in graph[current]:
                if neighbor not in visited:
                    heuristic = 0
                    new_transit_count = transit_count
                    new_lines = lines.copy()
                    if not lines or lines[-1] != line:
                        new_lines.append(line)
                        new_transit_count += 1 if lines else 0
                    heapq.heappush(queue, (total_distance + heuristic, neighbor, path + [neighbor], new_lines, total_distance + dist, total_cost + cost, total_duration + dur, new_transit_count))
    return None, None, None, None, None, None

# ------------------------------------------------------------------------------------
#                                  INPUT FROM USERS 
# ------------------------------------------------------------------------------------
print("\nWelcome to Shinkansen Route Planning Service! Please wait for a moment...\n")
start_station = input("Which station are you from ?: ")
goal_station = input("Which station you want to go to ?: ")
print("\nPlease select your primary travel preference:")
print("1. Fastest route (if you're in a rush)")
print("2. Least transit route (if carrying heavy items or tired)")
print("3. Cheapest route (if you're on a budget)")
choice = input("Enter the number of your preference (1, 2, or 3): ")

# Map user choice to criteria
if choice == '1':
    selected_criterion = 'fastest'
elif choice == '2':
    selected_criterion = 'least_transit'
elif choice == '3':
    selected_criterion = 'cheapest'
else:
    print("Invalid choice. Please restart and choose a valid option.")
    exit()

# Run each search with timing
print("\nCalculating the best route based on your preference...\n")

(dijkstra_path, dijkstra_lines, dijkstra_dist, dijkstra_cost, dijkstra_dur, dijkstra_transits), dijkstra_time = timed_search(dijkstra_search, graph, start_station, goal_station)
(transits_path, transits_lines, transits_dist, transits_cost, transits_dur, transits_transits), transits_time = timed_search(least_transits_search, graph, start_station, goal_station)
(bfs_path, bfs_lines, bfs_dist, bfs_cost, bfs_dur, bfs_transits), bfs_time = timed_search(bfs, graph, start_station, goal_station)
(best_first_path, best_first_lines, best_first_dist, best_first_cost, best_first_dur, best_first_transits), best_first_time = timed_search(best_first_search, graph, start_station, goal_station)

# Collect all routes in a list
routes = [
    (dijkstra_path, dijkstra_lines, dijkstra_dist, dijkstra_cost, dijkstra_dur, dijkstra_transits),
    (transits_path, transits_lines, transits_dist, transits_cost, transits_dur, transits_transits),
    (bfs_path, bfs_lines, bfs_dist, bfs_cost, bfs_dur, bfs_transits),
    (best_first_path, best_first_lines, best_first_dist, best_first_cost, best_first_dur, best_first_transits)
]

# Get the best route based on the user's chosen criterion
best_route = get_best_route(routes, selected_criterion)

# Display the best route
if best_route:
    path, lines, distance, cost, duration, transits = best_route
    print("\nBest Route Based on Your Preference:")
    print("Route:", " -> ".join(path))
    print("Lines:", " -> ".join(lines))
    print("Total Distance:", f"{distance:.2f}", "km")
    print("Total Cost:", f"{cost:.2f}", "Yen")
    print("Total Duration:", f"{duration:.2f}", "minutes")
    print("Total Transits:", transits)
else:
    print("No suitable route found based on your preference.")

print("\nThank you for using our service")
print("We wish you a safe journey!")
