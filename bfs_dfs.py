
from collections import deque

# Graph representation
graph = {
    'A': ['B', 'C'],
    'B': ['A', 'D'],
    'C': ['A', 'G'],
    'D': ['B', 'G'],
    'G': ['C', 'D']
}

# Breadth First Search
def bfs(graph, start, goal):
    queue = deque([[start]])
    visited = set()

    while queue:
        path = queue.popleft()
        node = path[-1]

        if node == goal:
            return path

        if node not in visited:
            visited.add(node)

            for neighbor in graph[node]:
                if neighbor not in visited:
                    queue.append(path + [neighbor])

    return None


# Depth First Search
def dfs(graph, start, goal):
    stack = [[start]]
    visited = set()

    while stack:
        path = stack.pop()
        node = path[-1]

        if node == goal:
            return path

        if node not in visited:
            visited.add(node)

            for neighbor in reversed(graph[node]):
                if neighbor not in visited:
                    stack.append(path + [neighbor])

    return None


# Main Program
start = 'A'
goal = 'G'

print("Breadth First Search (BFS)")
print("Path:", bfs(graph, start, goal))

print("\nDepth First Search (DFS)")
print("Path:", dfs(graph, start, goal))
