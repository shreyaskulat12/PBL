
from collections import deque

# Grid size
SIZE = 4

# Start and Goal
START = (1, 1)
GOAL = (4, 4)

# Obstacles
obstacles = {
    (2, 2),
    (2, 3),
    (3, 2)
}

# STRIPS Action Representation
actions = {
    "MoveUp": (0, 1),
    "MoveDown": (0, -1),
    "MoveLeft": (-1, 0),
    "MoveRight": (1, 0)
}


# Apply STRIPS action
def apply_action(state, action):

    x, y = state

    dx, dy = actions[action]

    new_state = (x + dx, y + dy)

    # Preconditions
    if not (1 <= new_state[0] <= SIZE):
        return None

    if not (1 <= new_state[1] <= SIZE):
        return None

    if new_state in obstacles:
        return None

    # Delete-list: At(x, y)
    # Add-list: At(new_x, new_y)

    return new_state


# BFS Planner
def bfs_planner(start, goal):

    queue = deque([start])

    visited = {start}

    parent = {start: (None, None)}

    while queue:

        current = queue.popleft()

        # Goal checking
        if current == goal:

            plan = []
            path = []

            while current is not None:

                path.append(current)

                previous, action = parent[current]

                if action is not None:
                    plan.append(action)

                current = previous

            return plan[::-1], path[::-1]

        # Generate next states
        for action in actions:

            new_state = apply_action(
                current, action
            )

            if new_state is not None:
                if new_state not in visited:

                    visited.add(new_state)

                    parent[new_state] = (
                        current, action
                    )

                    queue.append(new_state)

    return None, None


# Main Program
print("CLASSICAL PLANNING USING STRIPS")

plan, path = bfs_planner(START, GOAL)

if plan is not None:

    print("\nStart Position:", START)
    print("Goal Position:", GOAL)

    print("\nAction Plan:")

    for step, action in enumerate(plan, 1):
        print(step, action)

    print("\nPath:", path)

    print("\nTotal Actions:", len(plan))

else:
    print("No valid plan found.")
