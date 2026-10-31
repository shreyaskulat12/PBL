
from itertools import product

# Step 1: Define Bayesian Network

nodes = {
    "Rain": {
        "parents": [],
        "cpt": {(): 0.3}
    },

    "Wind": {
        "parents": [],
        "cpt": {(): 0.4}
    },

    "Picnic": {
        "parents": ["Rain", "Wind"],
        "cpt": {
            (False, False): 0.90,
            (False, True): 0.60,
            (True, False): 0.20,
            (True, True): 0.05
        }
    }
}

ORDER = ["Rain", "Wind", "Picnic"]


# Step 2: Calculate probability of True

def prob_true(var, assignment):

    parents = nodes[var]["parents"]

    key = tuple(assignment[p] for p in parents)

    return nodes[var]["cpt"][key]


# Step 3: Calculate Joint Probability

def joint_probability(assignment):

    p = 1.0

    for var in ORDER:

        p_true = prob_true(var, assignment)

        if assignment[var]:
            p *= p_true
        else:
            p *= (1 - p_true)

    return p


# Step 4: Generate all assignments

def all_assignments(variables):

    for values in product(
        [True, False], repeat=len(variables)
    ):

        yield dict(zip(variables, values))


# Step 5: Inference using Enumeration

def enumeration_ask(query_var, evidence):

    hidden_vars = [
        v for v in ORDER
        if v != query_var and v not in evidence
    ]

    scores = {}

    for query_value in [True, False]:

        total = 0.0

        for hidden_assignment in all_assignments(
            hidden_vars
        ):

            full_assignment = dict(hidden_assignment)

            full_assignment[query_var] = query_value

            full_assignment.update(evidence)

            total += joint_probability(full_assignment)

        scores[query_value] = total

    # Normalize using Bayes' Rule

    normalizer = sum(scores.values())

    return {
        k: v / normalizer
        for k, v in scores.items()
    }


# Step 6: Display Results

def show(dist, var_name):

    print(
        f"P({var_name} = True) = {dist[True]:.4f}"
    )

    print(
        f"P({var_name} = False) = {dist[False]:.4f}"
    )


# Step 7: Run Queries

print("Query 1: Overall chance of a picnic")

result1 = enumeration_ask("Picnic", {})

show(result1, "Picnic")


print("\nQuery 2: Chance of picnic when it is raining")

result2 = enumeration_ask(
    "Picnic", {"Rain": True}
)

show(result2, "Picnic")


print("\nQuery 3: Chance of rain when there is no picnic")

result3 = enumeration_ask(
    "Rain", {"Picnic": False}
)

show(result3, "Rain")
