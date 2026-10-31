
import re
import itertools

# --------------------------------
# 1. Parse First-Order Logic
# --------------------------------

def parse_atom(text):
    match = re.match(r"(\w+)\((.*)\)", text.strip())

    if not match:
        raise ValueError("Invalid FOL expression: " + text)

    predicate = match.group(1)
    args = tuple(
        arg.strip() for arg in match.group(2).split(",")
    )

    return (predicate, args)


def parse_rule(text):
    left, right = text.split("=>")

    premises = [
        parse_atom(p.strip())
        for p in left.split("&")
    ]

    conclusion = parse_atom(right.strip())

    return (premises, conclusion)


# --------------------------------
# 2. Unification
# --------------------------------

def is_variable(term):
    return term[0].islower()


def substitute(term, theta):
    while is_variable(term) and term in theta:
        term = theta[term]

    return term


def unify_terms(x, y, theta):

    x = substitute(x, theta)
    y = substitute(y, theta)

    if x == y:
        return theta

    if is_variable(x):
        theta[x] = y
        return theta

    if is_variable(y):
        theta[y] = x
        return theta

    return None


def unify_atoms(atom1, atom2, theta=None):

    if theta is None:
        theta = {}

    if atom1[0] != atom2[0]:
        return None

    if len(atom1[1]) != len(atom2[1]):
        return None

    theta = theta.copy()

    for x, y in zip(atom1[1], atom2[1]):

        theta = unify_terms(x, y, theta)

        if theta is None:
            return None

    return theta


def apply_substitution(atom, theta):

    return (
        atom[0],
        tuple(substitute(arg, theta) for arg in atom[1])
    )


def has_variables(atom):
    return any(is_variable(x) for x in atom[1])


# --------------------------------
# 3. Knowledge Base
# --------------------------------

fact_text = [
    "American(West)",
    "Missile(M1)",
    "Owns(Nono,M1)",
    "Enemy(Nono,America)"
]

rule_text = [
    "Missile(x) => Weapon(x)",

    "Enemy(x,America) => Hostile(x)",

    "Missile(x) & Owns(Nono,x) => Sells(West,x,Nono)",

    "American(x) & Weapon(y) & Sells(x,y,z) & Hostile(z) => Criminal(x)"
]

facts = set(parse_atom(f) for f in fact_text)

rules = [parse_rule(r) for r in rule_text]


# --------------------------------
# 4. Forward Chaining
# --------------------------------

def match_premises(premises, theta, known_facts):

    if not premises:
        yield theta
        return

    first = apply_substitution(premises[0], theta)

    for fact in known_facts:

        new_theta = unify_atoms(first, fact, theta)

        if new_theta is not None:

            yield from match_premises(
                premises[1:],
                new_theta,
                known_facts
            )


def forward_chaining(query):

    changed = True

    while changed:

        changed = False

        for premises, conclusion in rules:

            for theta in match_premises(
                premises, {}, list(facts)
            ):

                new_fact = apply_substitution(
                    conclusion, theta
                )

                if not has_variables(new_fact):

                    if new_fact not in facts:

                        facts.add(new_fact)
                        print("Derived:", new_fact)
                        changed = True

        if query in facts:
            return True

    return query in facts


# --------------------------------
# 5. Backward Chaining
# --------------------------------

counter = itertools.count()


def standardize_rule(rule):

    premises, conclusion = rule

    variables = set()

    for atom in premises + [conclusion]:
        for arg in atom[1]:
            if is_variable(arg):
                variables.add(arg)

    rename = {
        v: "v" + str(next(counter)) + v
        for v in variables
    }

    def rename_atom(atom):
        return (
            atom[0],
            tuple(rename.get(x, x) for x in atom[1])
        )

    return (
        [rename_atom(a) for a in premises],
        rename_atom(conclusion)
    )


def prove_all(goals, theta, depth=0):

    if not goals:
        yield theta
        return

    if depth > 30:
        return

    first = goals[0]
    remaining = goals[1:]

    for new_theta in prove(first, theta, depth):

        yield from prove_all(
            remaining, new_theta, depth + 1
        )


def prove(goal, theta, depth=0):

    if depth > 30:
        return

    goal = apply_substitution(goal, theta)

    # Check known facts
    for fact in facts:

        new_theta = unify_atoms(goal, fact, theta)

        if new_theta is not None:
            yield new_theta

    # Check rules
    for rule in rules:

        premises, conclusion = standardize_rule(rule)

        new_theta = unify_atoms(
            goal, conclusion, theta
        )

        if new_theta is not None:

            yield from prove_all(
                premises, new_theta, depth + 1
            )


def backward_chaining(query):

    return next(prove(query, {}), None) is not None


# --------------------------------
# 6. Main Program
# --------------------------------

print("FIRST-ORDER LOGIC REASONING")

# Unification example
print("\nUnification Example:")

atom1 = parse_atom("Loves(x,Mary)")
atom2 = parse_atom("Loves(John,Mary)")

print("Atom 1:", atom1)
print("Atom 2:", atom2)
print("Substitution:", unify_atoms(atom1, atom2))


# Forward Chaining
query = parse_atom("Criminal(West)")

print("\nForward Chaining:")
result1 = forward_chaining(query)
print("Criminal(West):", result1)


# Backward Chaining
print("\nBackward Chaining:")
result2 = backward_chaining(query)
print("Criminal(West):", result2)
