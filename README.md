# KKA-Final-Project

Group members:

| Name | NRP |
| ------------- |:-------------:|
| Muiz Surya Fata      | 5025231005    |
| Alfa Radithya Fanany      | 5025231008    |
| Muhammad Iqbal Shafarel      | 5025231080     |
| Ali Ridho      | 5025231162     |
| Faiz Adli Nugraha     | 5025231174    |

## A. Introduction

The efficiency of railway system plays an important role for public transportation, especially in urban areas like Tokyo. It enables everyone to reach their destination in the most efficient way possible. In this project, we will simulate that system using AI to find the shortest path and the most efficient ones. This will involve creating an AI pathfinding system that can improve route selection and train management to maximize the efficiency for anyone from Tokyo.

Transportation systems in large cities often face challenges such as inefficiency and delays, especially as population grows. These problems can lead to enviromental concerns, wasted time and also economic losses. To address these issues we can make use of advanced technologies like Artificial Intellegence to improve transportation quality. By analizing dataset from a railroad systems like for example the shinkansen (Japan’s high-speed rail network), AI can help optimize schedules and routes for trains to reach the destination

Optimizing Shinkansen rail track usage requires efficient search algorithms to enhance routing, scheduling, and energy management. The Best Search Algorithm helps identify optimal paths by considering factors such as travel time and cost-effectiveness, while BFS (Breadth-First Search) ensures all potential routes are explored, maximizing track utilization. A* algorithm, with its heuristic-based approach, further improves this by dynamically planning routes with an extended pre-sight, allowing it to anticipate future network conditions, such as congestion or track availability. This dynamic planning helps reduce delays and energy consumption by selecting routes that minimize accelerations, decelerations, and elevation changes, making the entire system more energy-efficient and cost-effective. The combination of these algorithms ensures that Shinkansen operations are optimized for both performance and sustainability, providing smoother operations while significantly reducing operational costs.

## B. Progress

### 1. Dataset
This dataset provides information about some of the Shinkansen high-speed rail network in Japan, detailing aspects of each station across various lines. The data spans multiple stations and lines, each with specific attributes such as the distance, fare, and duration of the travel. It supports various analyses, such as determining the most efficient routes, assessing travel costs for different distances, and examining the infrastructure's role in connecting key regions and cities in Japan. This data can be used by travelers, researchers, and transit planners to optimize travel experience, pricing strategies, and regional accessibility across the Shinkansen network.

- Source_Station:This column lists the departure station for each segment, which is the station where passengers would board the Shinkansen. Japan's Shinkansen network covers a vast number of stations, and each station serves as either a stop, origin, or destination depending on the route and segment.

- Shinkansen_Line: This indicates the specific Shinkansen line (e.g., Tokaido_Shinkansen) on which the station is located. Shinkansen lines often serve different regions and have unique stops, so this column helps differentiate routes when analyzing the network.

- Destination_Station: This shows the end station for the journey segment listed in the row. Each segment (route between two stations) has its own entry, and the destination station here can serve as a transfer point, final stop, or a midpoint depending on the passengers’s route.

- Distance_(Km): This column displays the distance in kilometers between the source and destination stations for each segment. Distance can directly influence ticket pricing and travel duration, though certain segments may vary slightly in speed or route efficiency.

- Cost_(Yen): This is the fare in Japanese yen between the source and destination stations for each segment. Different trains or lines can influence the price of the fare.

- Durations_(Min): This gives the travel time in minutes for each segment. Shinkansen speeds can vary between lines and services; for example, "Hayabusa" is a high-speed service on the Tohoku Shinkansen, known for its shorter travel times. Travel time in this column reflects these variations in speed and stop frequency for each segment.

- Line: This column identifies the specific service or type of Shinkansen running on the Shinkansen line. For example:

    - Asama: A service on the Hokuriku Shinkansen that operates between Tokyo and Nagano.
    - Hakutaka: Another service on the Hokuriku Shinkansen, which extends beyond Nagano to Kanazawa.
    - Hayabusa: A high-speed service on the Tohoku Shinkansen, running between Tokyo and northern destinations like Shin-Aomori.
Each line name indicates a unique train routes, speed and destinations.


### 2. Code Explanation

#### 2a. Graph Initialization
```python
import pandas as pd
import heapq
from collections import deque, defaultdict

# Load dataset
df = pd.read_csv('shinkansen.csv')

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
    graph[destination].append((source, line, distance, cost, duration))
```
The code begins by loading data from `shinkansen.csv`, a dataset containing details of railway routes. It then constructs a graph using Python’s `defaultdict` from the `collections` module, which stores lists of connected stations and associated travel information. For each row in the dataset, the code reads the `source` and `destination` stations, `line` name, `distance` (in kilometers), `cost` (in yen), and `duration` (in minutes) of travel. Each source station is mapped to its destination with all route details in a tuple, and because the graph is undirected, each route is added in both directions: from the source to the destination and from the destination back to the source.

#### 2b. Least Transit Search
```python
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
```
This function `least_transits_search` aims to find a route between two stations with the fewest line changes, using a Breadth-First Search (BFS) approach. It initializes queue as a deque containing tuples of the format `(station, path, lines, transit_count)`, where `station` is the current station, `path` is the list of stations visited, `lines` is a list of lines taken, and `transit_count` is the number of line changes so far. `visited` is a set that tracks each station and line combination visited to prevent redundant visits. For each neighbor, if the line changes, it increments `transit_count` and adds the line to `new_lines`. When the `destination` is reached, the function returns the `path`, `lines`, and `transit_count`.

#### 2c. Best First Search
```python
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
```
In the best_first_search function, a priority queue `queue` is used to implement the search, where each entry is a tuple of the format `(heuristic distance, station, path, lines, total_distance, total_cost, total_duration, transit_count)`. The `heuristic distance` helps prioritize stations closer to the goal. `station` is the current location, `path` is the sequence of stations visited, `lines` is the list of lines taken, `total_distance` is the cumulative distance, `total_cost` is the cumulative yen cost, `total_duration` is the travel time, and `transit_count` keeps track of line changes. For each neighbor, if the line is new, it’s added to `new_lines`, and `new_transit_count` is incremented if there’s a previous line. The function returns the optimal path with details if the goal is reached.

#### 2d. Breadth First Search
```python
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
```
The `bfs` function uses a queue to explore paths from the starting station to the destination, focusing on finding the shortest number of steps. Each element in the queue is a tuple of `(station, path, lines, total_distance, total_cost, total_duration, transit_count)`. `station` is the current station, `path` is the list of stations in the route, `lines` contains the lines used, `total_distance` accumulates the distance traveled, `total_cost` stores the total yen cost, `total_duration` tracks the time in minutes, and `transit_count` records line changes. When a line change is encountered, it’s added to `new_lines`, and `new_transit_count` is updated. This search is efficient for finding the shortest sequence of stations.

#### 2e. A* Search
```python
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
```    
The `a_star_search` function uses an A* search algorithm with distance-based heuristics to prioritize routes. It uses a priority queue where each tuple includes `(heuristic distance, station, path, lines, total_distance, total_cost, total_duration, transit_count)`. The `heuristic distance` is based on the neighbor distance to prioritize paths, while `station` is the current location, `path` is the visited sequence of stations, `lines` tracks the lines taken, `total_distance` accumulates the distance, `total_cost` is the yen cost, `total_duration` tracks time, and `transit_count` records the number of line changes. If a new line is encountered, it’s added to `new_lines`, and `new_transit_count` is incremented. This function balances minimizing both distance and line changes.

#### 2f. User Input
```python
print("\nWelcome to Shinkansen Route Planning Service! Please wait for a moment... \n")
start_station = input("Which station are you from ?: ")
goal_station = input("Which station you want to go to ?: ")
print("\nCalculating Route, Distance, Cost, and Duration... \n")
```
This section of the code begins by giving the user with a message about the Shinkansen Route Planning Service. It then prompts the user for input using `input()` to collect two pieces of information: `start_station` (the station they are departing from) and `goal_station` (their intended destination). This information is essential for performing the route search, as it specifies the `start` and `end` points for each search function to process.

#### 2h. How the results will be displayed
```python
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
```
After gathering user input and running each of the search functions (Best-First Search, BFS, A*, and Least Transits Search), the program displays the results for each search method. For each method:
- If a route is found, it prints the `path` (sequence of stations), `lines` (sequence of lines used), `total_distance` (in kilometers), `total_cost` (in yen), `total_duration` (in minutes), and `transit_count` (number of line changes).
- If no route is found, it outputs a message indicating that a route could not be determined.

### 3. Result

![image](https://github.com/user-attachments/assets/8fb3d2a3-3ae9-42a9-a35d-b5d9cbd261e8)

#### A. Best First Search : 
This method uses a heuristic approach to find the route that seems closest to the destination based on the shortest distance or certain priorities. This is a very long and winding route. The search seems to have prioritized certain larger stations, leading the path far south before it eventually redirects back north to reach Morioka. This is a less efficient route with many extra stops, including major cities like Nagoya, Kyoto, Shin-Osaka, Hakata, and Sendai. It shows how Best First Search can sometimes yield suboptimal routes due to its heavy reliance on heuristic guidance.

#### B. Breadth First Search (BFS) : 
BFS, which does not rely on heuristics, naturally discovers the shortest path in terms of the number of stations to traverse. This route is much more direct and stays mostly on the Tohoku Shinkansen line, which is the direct line connecting Tokyo to Morioka. This route explores fewer stations overall and avoids the southern stations completely, following a logical northward progression from Tokyo to Morioka. BFS guarantees a route with a minimum number of steps, but it is not always the shortest route in terms of distance.

#### C. A* Search : 
A* Search is a search method that combines the advantages of BFS and the heuristics in Best First Search. This algorithm considers the total distance from the starting point to the destination and selects a move that optimizes the overall path. The route it took is identical to the BFS route, because we haven't added the cost in the dataset yet. A* optimally balanced path cost and heuristic to yield a direct path similar to the BFS approach, using only the necessary intermediate stations along the Tohoku Shinkansen line without deviating to southern or distant stations. 

#### D. Conclusion:

Overall, these results indicate that BFS and A* Search provide more efficient routes than Best First Search in this case, especially because they produce fewer intermediate stations to reach the destination in Morioka.
