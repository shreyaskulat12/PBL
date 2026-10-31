
# Wumpus World using Propositional Logic
# and Forward Chaining

SIZE = 4

# Hidden locations
PITS = {(4, 4)}
WUMPUS = (4, 1)
GOLD = (1, 4)

START = (1, 1)

# Generate all grid cells
all_cells = {
    (r, c)
    for r in range(1, SIZE + 1)
    for c in range(1, SIZE + 1)
}

# Knowledge Base
possible_pits = all_cells - {START}
possible_wumpus = all_cells - {START}

visited = set()
safe_cells = {START}


# Find neighboring cells
def get_neighbors(cell):

    r, c = cell

    directions = [
        (-1, 0),
        (1, 0),
        (0, -1),
        (0, 1)
    ]

    neighbors = []

    for dr, dc in directions:

        nr = r + dr
        nc = c + dc

        if 1 <= nr <= SIZE and 1 <= nc <= SIZE:
            neighbors.append((nr, nc))

    return neighbors


# Observe percepts
def perceive(cell):

    neighbors = get_neighbors(cell)

    breeze = any(n in PITS for n in neighbors)

    stench = any(n == WUMPUS for n in neighbors)

    glitter = (cell == GOLD)

    return breeze, stench, glitter


# Forward Chaining
def forward_chaining():

    while True:

        old_safe = set(safe_cells)

        for cell in visited:

            breeze, stench, glitter = perceive(cell)

            neighbors = get_neighbors(cell)

            # Rule 1: No Breeze
            if not breeze:
                possible_pits.difference_update(neighbors)

            # Rule 2: No Stench
            if not stench:
                possible_wumpus.difference_update(neighbors)

        # Rule 3: Mark Safe Cells
        for cell in all_cells:

            if (cell not in possible_pits
                    and cell not in possible_wumpus):

                safe_cells.add(cell)

        # Stop at fixed point
        if safe_cells == old_safe:
            break


# Wumpus World Agent
def wumpus_agent():

    current = START

    print("WUMPUS WORLD SIMULATOR")
    print("Agent starts at:", START)

    while True:

        visited.add(current)

        # Current cell is safe because agent survived
        possible_pits.discard(current)
        possible_wumpus.discard(current)

        breeze, stench, glitter = perceive(current)

        print("\nVisiting:", current)
        print("Breeze:", breeze)
        print("Stench:", stench)
        print("Glitter:", glitter)

        # Check for gold
        if glitter:
            print("\nGOLD FOUND!")
            print("Agent successfully completed the mission.")
            break

        # Apply Forward Chaining
        forward_chaining()

        # Find safe unvisited cells
        next_cells = sorted(safe_cells - visited)

        print("Safe unvisited cells:", next_cells)

        # No safe cell available
        if not next_cells:
            print("\nNo safe cells left to explore.")
            break

        # Move to next safe cell
        current = next_cells[0]

    print("\nVisited Cells:", sorted(visited))


# Main Program
wumpus_agent()
