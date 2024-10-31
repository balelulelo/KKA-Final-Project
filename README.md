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
###
### 2. Code Explanation

#### 2a. Calling All Libraries

```python
import pandas as pd
import heapq
from collections import deque
```
`pandas`: Used to handle CSV data for loading from a file.
`heapq`: Provides priority queue functionality essential for the `Best-First Search` and `A* Search algorithms`.
`deque`: Used for efficiently implementing the `queue structure` required for `Breadth-First Search`.

#### 2b. Graph Initialization
```python
class Graph:
    def __init__(self):
        self.graph = {}
        self.heuristics = {}
```
- `Graph`: A class representing the railway network.
- `graph`: store each station and its connections with other stations.
- `heuristics`: storing heuristic values for each station, such as its distance from Tokyo.

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
