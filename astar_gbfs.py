
import heapq
import itertools

# 2D Grid
grid = [
    ['S', '.', '.', 'X', '.'],
    ['.', 'X', '.', 'X', '.'],
    ['.', '.', '.', '.', '.'],
    ['X', 'X', '.', 'X', '.'],
    ['.', '.', '.', '.', 'G']
]

start = (0, 0)
goal = (4, 4)

# Manhattan Distance
def heuristic(node):
    return abs(node[0] - goal[0]) + abs(node[1] - goal[1])


# Check valid movement
def get_neighbors(node):
    directions = [(-1, 0), (1, 0),
                   (0, -1), (0, 1)]

    neighbors = []

    for dr, dc in directions:
        r = node[0] + dr
        c = node[1] + dc

        if (0 <= r < 5 and 0 <= c < 5
                and grid[r][c] != 'X'):
            neighbors.append((r, c))

    return neighbors


# Reconstruct path
def get_path(parent, node):
    path = []

    while node is not None:
        path.append(node)
        node = parent[node]

    return path[::-1]


# Greedy Best-First Search
def greedy_best_first_search():

    counter = itertools.count()
    pq = [(heuristic(start), next(counter), start)]

    visited = set()
    parent = {start: None}

    while pq:
        _, _, current = heapq.heappop(pq)

        if current in visited:
            continue

        if current == goal:
            return get_path(parent, current)

        visited.add(current)

        for neighbor in get_neighbors(current):

            if neighbor not in visited and neighbor not in parent:
                parent[neighbor] = current

                heapq.heappush(
                    pq,
                    (heuristic(neighbor),
                     next(counter), neighbor)
                )

    return None


# A* Search
def a_star_search():

    counter = itertools.count()

    pq = [(heuristic(start), next(counter), start)]

    g_cost = {start: 0}
    parent = {start: None}
    visited = set()

    while pq:
        _, _, current = heapq.heappop(pq)

        if current in visited:
            continue

        if current == goal:
            return get_path(parent, current)

        visited.add(current)

        for neighbor in get_neighbors(current):

            new_g = g_cost[current] + 1

            if new_g < g_cost.get(neighbor, float('inf')):

                g_cost[neighbor] = new_g
                parent[neighbor] = current

                f = new_g + heuristic(neighbor)

                heapq.heappush(
                    pq,
                    (f, next(counter), neighbor)
                )

    return None


# Main Program
print("Greedy Best-First Search:")
print(greedy_best_first_search())

print("\nA* Search:")
print(a_star_search())
