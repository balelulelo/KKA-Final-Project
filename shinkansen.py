import pandas as pd
import heapq
from collections import deque

class Graph:
    def __init__(self):
        self.graph = {}
        self.heuristics = {}

    def add_edge(self, start, end, cost):
        if start not in self.graph:
            self.graph[start] = []
        self.graph[start].append((end, cost))

    def set_heuristic(self, node, value):
        self.heuristics[node] = value

    def best_first_search(self, start, goal):
        open_list = []
        heapq.heappush(open_list, (self.heuristics[start], start))
        closed_list = set()
        path = []

        while open_list:
            _, current = heapq.heappop(open_list)
            path.append(current)

            if current in closed_list:
                continue
            closed_list.add(current)

            if current == goal:
                return path

            for neighbor, cost in self.graph[current]:
                if neighbor not in closed_list:
                    heapq.heappush(open_list, (self.heuristics.get(neighbor, float('inf')), neighbor))

        return None

    def bfs(self, start, goal):
        queue = deque([(start, [start])])
        visited = set([start])

        while queue:
            current, path = queue.popleft()

            if current == goal:
                return path

            for neighbor, _ in self.graph[current]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))

        return None

    def a_star(self, start, goal):
        open_list = []
        heapq.heappush(open_list, (0 + self.heuristics[start], start, [start]))
        g_costs = {start: 0}

        while open_list:
            _, current, path = heapq.heappop(open_list)

            if current == goal:
                return path

            for neighbor, cost in self.graph[current]:
                new_g_cost = g_costs[current] + cost
                if neighbor not in g_costs or new_g_cost < g_costs[neighbor]:
                    g_costs[neighbor] = new_g_cost
                    f_cost = new_g_cost + self.heuristics.get(neighbor, float('inf'))
                    heapq.heappush(open_list, (f_cost, neighbor, path + [neighbor]))

        return None

# Membaca data dari CSV
def load_shinkansen_data(filename):
    data = pd.read_csv(filename)
    graph = Graph()

    # Membuat edge berdasarkan jarak antar stasiun
    for i in range(len(data) - 1):
        start_station = data.iloc[i]['Station_Name']
        end_station = data.iloc[i + 1]['Station_Name']
        distance = abs(data.iloc[i + 1]['Distance from Tokyo st'] - data.iloc[i]['Distance from Tokyo st'])

        graph.add_edge(start_station, end_station, distance)
        graph.add_edge(end_station, start_station, distance)  # Assuming bidirectional travel

    # Menambahkan heuristik (Distance from Tokyo st)
    for index, row in data.iterrows():
        graph.set_heuristic(row['Station_Name'], row['Distance from Tokyo st'])

    return graph

# Load graph dari CSV
filename = r"C:\Users\LENOVO\Codes in general\Kuliah di ITS\SMT 3\KKA\FP\shinkansen.csv"
graph = load_shinkansen_data(filename)

# Meminta input dari pengguna
start = input("Masukkan stasiun awal: ")  # Ganti dengan stasiun awal
goal = input("Masukkan stasiun tujuan: ")  # Ganti dengan stasiun tujuan

# Menjalankan pencarian
best_first_path = graph.best_first_search(start, goal)
bfs_path = graph.bfs(start, goal)
a_star_path = graph.a_star(start, goal)

# Menampilkan hasil dengan format yang diinginkan
def display_route(route):
    if route:
        print(" -> ".join(route))
    else:
        print("Rute tidak ditemukan.")

print("Best First Search:", end=' ')
display_route(best_first_path)

print("BFS:", end=' ')
display_route(bfs_path)

print("A* Search:", end=' ')
display_route(a_star_path)
