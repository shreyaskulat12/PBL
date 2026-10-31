
# Map Coloring using CSP

variables = ['A', 'B', 'C', 'D']

domains = {
    'A': ['Red', 'Green', 'Blue'],
    'B': ['Red', 'Green', 'Blue'],
    'C': ['Red', 'Green', 'Blue'],
    'D': ['Red', 'Green', 'Blue']
}

# Neighbor relationships
graph = {
    'A': ['B', 'C'],
    'B': ['A', 'C', 'D'],
    'C': ['A', 'B', 'D'],
    'D': ['B', 'C']
}


# Check constraints
def is_valid(variable, color, assignment):

    for neighbor in graph[variable]:

        if neighbor in assignment:
            if assignment[neighbor] == color:
                return False

    return True


# Backtracking Algorithm
def backtracking(assignment):

    if len(assignment) == len(variables):
        return assignment

    for variable in variables:

        if variable not in assignment:
            break

    for color in domains[variable]:

        if is_valid(variable, color, assignment):

            assignment[variable] = color

            result = backtracking(assignment)

            if result:
                return result

            del assignment[variable]

    return None


# Forward Checking Algorithm
def forward_checking(assignment, current_domains):

    if len(assignment) == len(variables):
        return assignment

    for variable in variables:

        if variable not in assignment:
            break

    for color in current_domains[variable]:

        if is_valid(variable, color, assignment):

            assignment[variable] = color

            # Copy domains
            new_domains = {
                v: list(current_domains[v])
                for v in variables
            }

            # Remove color from neighbors
            failure = False

            for neighbor in graph[variable]:

                if neighbor not in assignment:

                    if color in new_domains[neighbor]:
                        new_domains[neighbor].remove(color)

                    if len(new_domains[neighbor]) == 0:
                        failure = True
                        break

            if not failure:

                result = forward_checking(
                    assignment, new_domains
                )

                if result:
                    return result

            del assignment[variable]

    return None


# Main Program
print("MAP COLORING USING CSP")

print("\n1. Backtracking Result:")
result1 = backtracking({})

print(result1)

print("\n2. Forward Checking Result:")
result2 = forward_checking({}, domains)

print(result2)
