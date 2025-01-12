import networkx as nx
import matplotlib.pyplot as plt
from collections import deque

G = nx.DiGraph()

edges = [
    ('Terminal_1', 'Warehouse_1', 25),
    ('Terminal_1', 'Warehouse_2', 20),
    ('Terminal_1', 'Warehouse_3', 15),
    ('Terminal_2', 'Warehouse_3', 15),
    ('Terminal_2', 'Warehouse_4', 30),
    ('Terminal_2', 'Warehouse_2', 10),
    ('Warehouse_1', 'Shop_1', 15),
    ('Warehouse_1', 'Shop_2', 10),
    ('Warehouse_1', 'Shop_3', 20),
    ('Warehouse_2', 'Shop_4', 15),
    ('Warehouse_2', 'Shop_5', 10),
    ('Warehouse_2', 'Shop_6', 25),
    ('Warehouse_3', 'Shop_7', 20),
    ('Warehouse_3', 'Shop_8', 15),
    ('Warehouse_3', 'Shop_9', 10),
    ('Warehouse_4', 'Shop_10', 20),
    ('Warehouse_4', 'Shop_11', 10),
    ('Warehouse_4', 'Shop_12', 15),
    ('Warehouse_4', 'Shop_13', 5),
    ('Warehouse_4', 'Shop_14', 10),
]

G.add_weighted_edges_from(edges)

pos = {
    'Terminal_1': (-1, 0),
    'Terminal_2': (1, 0),

    'Warehouse_1': (-2, 2),
    'Warehouse_2': (2, 2),

    'Shop_1': (-3, 4),
    'Shop_2': (-2.5, 4),
    'Shop_3': (-2, 4),
    'Shop_4': (1, 4),
    'Shop_5': (1.5, 4),
    'Shop_6': (2, 4),

    'Warehouse_3': (-2, -2),
    'Warehouse_4': (2, -2),

    'Shop_7': (-3, -4),
    'Shop_8': (-2.5, -4),
    'Shop_9': (-2, -4),
    'Shop_10': (1, -4),
    'Shop_11': (1.5, -4),
    'Shop_12': (2, -4),
    'Shop_13': (2.5, -4),
    'Shop_14': (3, -4),
}



plt.figure(figsize=(10, 6))
nx.draw(G, pos, with_labels=True, node_size=2000, node_color="skyblue", font_size=12, font_weight="bold", arrows=True)
labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)

# Відображаємо граф
plt.show()


# Функція для пошуку збільшуючого шляху (BFS)
def bfs(capacity_matrix, flow_matrix, source, sink, parent):
    visited = [False] * len(capacity_matrix)
    queue = deque([source])
    visited[source] = True

    while queue:
        current_node = queue.popleft()
        
        for neighbor in range(len(capacity_matrix)):
            # Перевірка, чи є залишкова пропускна здатність у каналі
            if not visited[neighbor] and capacity_matrix[current_node][neighbor] - flow_matrix[current_node][neighbor] > 0:
                parent[neighbor] = current_node
                visited[neighbor] = True
                if neighbor == sink:
                    return True
                queue.append(neighbor)
    
    return False

# Основна функція для обчислення максимального потоку
def edmonds_karp(capacity_matrix, source, sink):
    num_nodes = len(capacity_matrix)
    flow_matrix = [[0] * num_nodes for _ in range(num_nodes)]  # Ініціалізуємо матрицю потоку нулем
    parent = [-1] * num_nodes
    max_flow = 0

    # Поки є збільшуючий шлях, додаємо потік
    while bfs(capacity_matrix, flow_matrix, source, sink, parent):
        # Знаходимо мінімальну пропускну здатність уздовж знайденого шляху (вузьке місце)
        path_flow = float('Inf')
        current_node = sink

        while current_node != source:
            previous_node = parent[current_node]
            path_flow = min(path_flow, capacity_matrix[previous_node][current_node] - flow_matrix[previous_node][current_node])
            current_node = previous_node
        
        # Оновлюємо потік уздовж шляху, враховуючи зворотний потік
        current_node = sink
        while current_node != source:
            previous_node = parent[current_node]
            flow_matrix[previous_node][current_node] += path_flow
            flow_matrix[current_node][previous_node] -= path_flow
            current_node = previous_node
        
        # Збільшуємо максимальний потік
        max_flow += path_flow

    return max_flow

# Матриця пропускної здатності для каналів у мережі (capacity_matrix)
capacity_matrix = [
    [0, 0, 25, 20, 15, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # Terminal 1
    [0, 0, 0, 10, 15, 30, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],   # Terminal 2
    [0, 0, 0, 0, 0, 0, 15, 10, 20, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],   # Warehouse 1
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 15, 10, 25, 0, 0, 0, 0, 0, 0, 0, 0],   # Warehouse 2
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 20, 15, 10, 0, 0, 0, 0, 0],   # Warehouse 3
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 20, 10, 15, 5, 10],   # Warehouse 4
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],    # Shop 1
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],    # Shop 2
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],     # Shop 3
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],    # Shop 4
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],    # Shop 5
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],    # Shop 6
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],    # Shop 7
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],    # Shop 8
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],    # Shop 9
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],    # Shop 10
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],    # Shop 11
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],    # Shop 12
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],    # Shop 13
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],    # Shop 14
]

source = [0, 1]  # Джерело 1
sink = [6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]    # Споживач 3

print("Термінал\tМагазин\tФактичний потік (одиниць)")

for s in source:
    for i in sink:
        terminal = f"Terminal_{s + 1}"
        shop = f"Shop_{i - 5}"
        flow = edmonds_karp(capacity_matrix, s, i)
        print(f"{terminal}\t{shop}\t{flow}")
