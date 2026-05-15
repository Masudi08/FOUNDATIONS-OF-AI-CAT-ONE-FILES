# Task 2b - Constraint Satisfaction Problem
# Map Colouring: Nairobi's 17 Sub-Counties
# Goal: Use the LEAST possible number of colours — no two adjacent sub-counties same colour
# Author: CCS 2226 Foundations of AI

from constraint import Problem

def solve_nairobi_colouring(num_colours):
    """Try to solve Nairobi colouring with a given number of colours."""
    problem = Problem()

    # Nairobi's 17 sub-counties
    subcounties = [
        "Westlands",
        "Dagoretti North",
        "Dagoretti South",
        "Langata",
        "Kibra",
        "Roysambu",
        "Kasarani",
        "Ruaraka",
        "Embakasi South",
        "Embakasi North",
        "Embakasi Central",
        "Embakasi East",
        "Embakasi West",
        "Makadara",
        "Kamukunji",
        "Starehe",
        "Mathare",
    ]

    colours = [f"Colour{i+1}" for i in range(num_colours)]
    colour_names = {
        "Colour1": "Blue",
        "Colour2": "Red",
        "Colour3": "Green",
        "Colour4": "Yellow",
    }

    for sc in subcounties:
        problem.addVariable(sc, colours)

    # Adjacency map based on Nairobi's geography
    adjacencies = [
        ("Westlands", "Roysambu"),
        ("Westlands", "Kasarani"),
        ("Westlands", "Dagoretti North"),
        ("Westlands", "Starehe"),
        ("Dagoretti North", "Dagoretti South"),
        ("Dagoretti North", "Kibra"),
        ("Dagoretti North", "Starehe"),
        ("Dagoretti South", "Kibra"),
        ("Dagoretti South", "Langata"),
        ("Langata", "Kibra"),
        ("Langata", "Embakasi West"),
        ("Kibra", "Embakasi West"),
        ("Kibra", "Makadara"),
        ("Roysambu", "Kasarani"),
        ("Roysambu", "Mathare"),
        ("Roysambu", "Starehe"),
        ("Kasarani", "Ruaraka"),
        ("Kasarani", "Embakasi North"),
        ("Kasarani", "Mathare"),
        ("Ruaraka", "Embakasi North"),
        ("Ruaraka", "Mathare"),
        ("Embakasi North", "Embakasi Central"),
        ("Embakasi North", "Embakasi East"),
        ("Embakasi Central", "Embakasi South"),
        ("Embakasi Central", "Embakasi East"),
        ("Embakasi Central", "Embakasi West"),
        ("Embakasi Central", "Makadara"),
        ("Embakasi East", "Embakasi South"),
        ("Embakasi West", "Makadara"),
        ("Embakasi West", "Embakasi South"),
        ("Makadara", "Kamukunji"),
        ("Makadara", "Starehe"),
        ("Kamukunji", "Starehe"),
        ("Kamukunji", "Mathare"),
        ("Starehe", "Mathare"),
    ]

    for sc1, sc2 in adjacencies:
        problem.addConstraint(
            lambda c1, c2: c1 != c2,
            (sc1, sc2)
        )

    return problem.getSolution(), adjacencies, colour_names, subcounties

def main():
    print("=" * 60)
    print("  NAIROBI SUB-COUNTIES MAP COLOURING (CSP)")
    print("  Goal: Minimum colours, no adjacent sub-counties same colour")
    print("=" * 60)

    # Try from 2 colours upward until a solution is found
    for n in range(2, 6):
        print(f"\n  Trying with {n} colour(s)...", end=" ")
        solution, adjacencies, colour_names, subcounties = solve_nairobi_colouring(n)
        if solution:
            print(f"✓ SOLUTION FOUND with {n} colours!\n")
            print(f"  Minimum colours needed: {n}")
            print("-" * 60)
            for sc in subcounties:
                raw = solution[sc]
                name = colour_names.get(raw, raw)
                print(f"  {sc:<25} → {name}")
            print("=" * 60)

            # Verify no adjacency conflicts
            print("\n  Adjacency Verification:")
            print("-" * 60)
            conflicts = 0
            for sc1, sc2 in adjacencies:
                c1 = colour_names.get(solution[sc1], solution[sc1])
                c2 = colour_names.get(solution[sc2], solution[sc2])
                if solution[sc1] == solution[sc2]:
                    print(f"  ✗ CONFLICT: {sc1} ({c1}) — {sc2} ({c2})")
                    conflicts += 1
            if conflicts == 0:
                print(f"  ✓ All {len(adjacencies)} adjacency constraints satisfied. No conflicts!")
            print("=" * 60)
            break
        else:
            print("No solution.")

if __name__ == "__main__":
    main()