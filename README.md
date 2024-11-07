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
This dataset provides comprehensive information about the Shinkansen high-speed rail network in Japan, detailing key aspects of each station across various lines. The data spans multiple stations and lines, each with specific attributes such as location, operational history, and company ownership. This allows for a thorough exploration of the Shinkansen's structure, from its geographic distribution across Japanese prefectures to the distances between stations relative to Tokyo, the central hub. By integrating these fields, the dataset supports in-depth analysis and can aid in optimizing search algorithms

- Station_Name: This column lists the names of each Shinkansen station. It identifies the specific station on a given Shinkansen line and serves as a unique point in any route or search algorithm.

- Shinkansen_Line: This indicates the specific Shinkansen line (e.g., Tokaido_Shinkansen) on which the station is located. Shinkansen lines often serve different regions and have unique stops, so this column helps differentiate routes when analyzing the network.

- Year: This column shows the year each station was opened. It could be useful for historical analysis, for example, to see how the Shinkansen network has expanded over time
- Prefecture: This specifies the Japanese prefecture where each station is located. It helps in understanding the geographical distribution of stations across Japan and can be useful if routes or search algorithms are organized by regional constraints.

- Distance from Tokyo st: This represents the distance of each station from Tokyo Station, measured in kilometers. This column is valuable for search algorithms as it can act as a heuristic measure, especially in Best First Search, to determine proximity to Tokyo or prioritize closer stations.

- Company: This indicates the company that operates each station. In Japan, different segments of the Shinkansen network are operated by different companies (e.g., JR Central). This could be relevant for financial or operational analysis, or for understanding corporate boundaries within the network.

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
The code begins by loading a dataset (shinkansen.csv) and constructing a graph of the railway network using a defaultdict. Each station (source) is connected to a destination, along with route details such as line, distance, cost, and duration. The graph is built to be undirected, so each route is bi-directional. Each station in the graph thus holds a list of tuples that store all available routes to neighboring stations

#### 2c. Function to Add an Edge
```python
def add_edge(self, start, end, cost):
    if start not in self.graph:
        self.graph[start] = []
    self.graph[start].append((end, cost))
```
- `add_edge`: Adds a route between two stations with a specified travel cost (distance).
- `start`: The originating station.
- `end`: The destination station.
- `cost`: The travel cost (distance) between the stations.
- Checks if the start station is already in the `graph`. If not, initializes an empty list for it.
- Adds the destination station (end) and cost as a tuple to the start station’s adjacency list.

#### 2d. Setting the Heuristic Function
```python
def set_heuristic(self, node, value):
    self.heuristics[node] = value
```
- `set_heuristic`: Sets the heuristic value for a station (node).
- This function use for `Best-First` and `A* algorithms` by assigning `heuristic values` for better prioritization based on proximity to the goal.

#### 2e. How Best-First Search Works
```python
def best_first_search(self, start, goal):
    open_list = []
    heapq.heappush(open_list, (self.heuristics[start], start))
    closed_list = set()
    path = []
```
- `best_first_search`: Uses a priority queue (heap) to explore nodes with the smallest heuristic values first.
- `open_list`: Holds stations to explore, prioritized by heuristic values.
- `closed_list`: Tracks visited stations to prevent re-exploration.
- If the current station matches the goal, the function returns the path.
Otherwise, it examines neighboring stations and adds them to `open_list` if they aren’t in `closed_list`.

#### 2f. How Breadth-First Search (BFS) Works (Not Optimal Yet)
```python
def bfs(self, start, goal):
    queue = deque([(start, [start])])
    visited = set([start])
```    
- `bfs`: Uses a deque to implement BFS algorithm.
- `queue`: Holds each station with its path taken so far.
- `visited`: Tracks visited stations to avoid revisiting them.
- Returns the path if the goal is found, otherwise, explores all neighbors.
- This function are still not optimal because there is not cost for each route databases.

#### 2g. A* Search Algorithm (Not Optimal Yet)
```python
def a_star(self, start, goal):
    open_list = []
    heapq.heappush(open_list, (0 + self.heuristics[start], start, [start]))
    g_costs = {start: 0}
```
- `a_star`: Combines g_cost (cost from the start) and heuristics (estimated cost to the goal).
- `g_costs`: tracking the cost from the start to each station.
- `open_list`: Priority queue containing stations and their calculated `f_cost` (combined `g_cost` and `heuristic`).
- When the goal station is found, the function returns the path, guaranteeing the shortest route due to its optimal cost evaluation.
- Same with Best First Search, this function are not optimal because there is not cost for each route databases.

#### 2h. How BFS Function Works
```python
def bfs(self, start, goal):
    queue = deque([(start, [start])])
    visited = set([start])
```
- Searches level by level, for finding the shortest unweighted path.
- Starts from the start station and explores each level completely before moving deeper.
- If it finds the goal station, it returns the path.

#### 2i. How A* Function Works
```python
def a_star(self, start, goal):
    open_list = []
    heapq.heappush(open_list, (0 + self.heuristics[start], start, [start]))
    g_costs = {start: 0}
```
- `A*` finds the shortest weighted path from start to goal, factoring both travel cost and heuristic value.
- `open_list`: A priority queue containing stations and their calculated f_cost.
- The function returns the path once goal is reached, ensuring the shortest route due to its optimal cost evaluation.

#### 2j. Function to Load Shinkansen Data
```python
def load_shinkansen_data(filename):
    data = pd.read_csv(filename)
    graph = Graph()
```
- `load_shinkansen_data`: Reads station data from a CSV file and initializes the Graph.
- For each station, adds bidirectional routes based on distance. Sets heuristic values (distance from Tokyo) for each station.

#### 2k. Function to Display the Route
```python
def display_route(route):
    if route:
        print(" -> ".join(route))
    else:
        print("Rute tidak ditemukan.")
```
- `display_route`: Prints the path from start to goal.
- Joins each station in route with arrows `(->)`` for better direction readability.
- If no route is found, outputs `"Rute tidak ditemukan."`

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
