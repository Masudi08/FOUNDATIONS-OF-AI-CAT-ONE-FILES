# =============================================================================
# VACUUM CLEANER AGENT
# =============================================================================
# An intelligent reflex agent that perceives the cleanliness of room locations
# and acts accordingly — cleaning dirty rooms and moving between locations.
#
# Environment:
#   - A grid of rooms (default: 2x2 but scalable to NxN)
#   - Each room is either DIRTY or CLEAN
#   - The agent starts at a given position and navigates all rooms
#
# Agent Type: Simple Reflex Agent
#   - Percept  : current location + its cleanliness status
#   - Action   : CLEAN (if dirty) | MOVE (if clean)
#   - Goal     : all rooms clean
# =============================================================================

import random
import time

# ── Constants ────────────────────────────────────────────────────────────────
DIRTY = "DIRTY"
CLEAN = "CLEAN"

# ── Environment Setup ────────────────────────────────────────────────────────

def create_environment(rows, cols, dirt_probability=0.6):
    """
    Create a grid environment where each cell represents a room.
    Each room is randomly assigned DIRTY or CLEAN based on dirt_probability.

    Args:
        rows (int): Number of rows in the grid.
        cols (int): Number of columns in the grid.
        dirt_probability (float): Likelihood (0–1) that a room starts dirty.

    Returns:
        dict: A dictionary mapping (row, col) -> status (DIRTY or CLEAN)
    """
    environment = {}
    for r in range(rows):
        for c in range(cols):
            # Randomly assign status based on probability
            status = DIRTY if random.random() < dirt_probability else CLEAN
            environment[(r, c)] = status
    return environment


def display_environment(environment, rows, cols, agent_pos):
    """
    Visually display the current state of the environment grid.
    Shows agent position (🤖), dirty rooms (💩), and clean rooms (✅).

    Args:
        environment (dict): The grid of rooms and their statuses.
        rows (int): Number of rows.
        cols (int): Number of columns.
        agent_pos (tuple): Current (row, col) position of the agent.
    """
    print("\n  " + "  ".join(f" C{c}" for c in range(cols)))
    for r in range(rows):
        row_display = f"R{r} "
        for c in range(cols):
            if (r, c) == agent_pos:
                row_display += " 🤖 "   # Agent's current position
            elif environment[(r, c)] == DIRTY:
                row_display += " 💩 "   # Dirty room
            else:
                row_display += " ✅ "   # Clean room
        print(row_display)
    print()


# ── Sensors ──────────────────────────────────────────────────────────────────

def sense(environment, position):
    """
    SENSOR: The agent perceives the cleanliness of its current location.

    Args:
        environment (dict): The current state of all rooms.
        position (tuple): Agent's current (row, col).

    Returns:
        str: DIRTY or CLEAN status of the current room.
    """
    return environment[position]


# ── Actuators ─────────────────────────────────────────────────────────────────

def clean(environment, position):
    """
    ACTUATOR: Clean the current room by setting its status to CLEAN.

    Args:
        environment (dict): The room grid (mutated in place).
        position (tuple): Room to clean.
    """
    environment[position] = CLEAN
    print(f"    [ACTION] 🧹 Cleaned room {position}")


def move(position, next_position):
    """
    ACTUATOR: Move the agent from current position to the next room.

    Args:
        position (tuple): Current (row, col).
        next_position (tuple): Target (row, col).

    Returns:
        tuple: The new position after moving.
    """
    print(f"    [ACTION] 🚶 Moved from {position} → {next_position}")
    return next_position


# ── Navigation ────────────────────────────────────────────────────────────────

def get_traversal_order(rows, cols):
    """
    Generate a boustrophedon (snake/zigzag) traversal order over the grid.
    This ensures every room is visited exactly once — an efficient coverage path.

    Example for 3x3:
        (0,0) → (0,1) → (0,2)
        (1,2) → (1,1) → (1,0)   ← reversed on odd rows
        (2,0) → (2,1) → (2,2)

    Args:
        rows (int): Grid rows.
        cols (int): Grid columns.

    Returns:
        list: Ordered list of (row, col) tuples to visit.
    """
    order = []
    for r in range(rows):
        row_cells = [(r, c) for c in range(cols)]
        if r % 2 == 1:
            row_cells.reverse()   # Alternate direction on odd rows
        order.extend(row_cells)
    return order


# ── Agent Brain (Decision Function) ──────────────────────────────────────────

def agent_decision(percept):
    """
    AGENT FUNCTION: Maps a percept (room status) to an action decision.
    This is the core intelligence of the simple reflex agent.

    Rule table:
        If room is DIRTY → CLEAN
        If room is CLEAN → MOVE (handled by traversal loop)

    Args:
        percept (str): DIRTY or CLEAN.

    Returns:
        str: "CLEAN" or "MOVE"
    """
    if percept == DIRTY:
        return "CLEAN"
    else:
        return "MOVE"


# ── Main Agent Loop ───────────────────────────────────────────────────────────

def run_vacuum_agent(rows=2, cols=2, dirt_probability=0.6):
    """
    Main entry point for the Vacuum Cleaner Agent.
    Initializes the environment, then runs the agent through all rooms
    using a boustrophedon traversal pattern until all rooms are clean.

    Args:
        rows (int): Grid height (number of rows).
        cols (int): Grid width (number of columns).
        dirt_probability (float): Probability a room starts dirty.
    """
    print("=" * 55)
    print("       VACUUM CLEANER AGENT — SIMULATION START")
    print("=" * 55)

    # Step 1: Create the environment
    environment = create_environment(rows, cols, dirt_probability)

    # Step 2: Place agent at top-left corner
    agent_pos = (0, 0)

    print(f"\n📐 Grid size     : {rows} rows × {cols} cols")
    print(f"🎲 Dirt prob.    : {int(dirt_probability * 100)}%")
    print(f"📍 Start position: {agent_pos}")
    print(f"\n{'─'*55}")
    print("  INITIAL ENVIRONMENT STATE:")
    display_environment(environment, rows, cols, agent_pos)

    # Step 3: Get the order in which all rooms will be visited
    traversal = get_traversal_order(rows, cols)

    # Performance tracking
    steps = 0
    rooms_cleaned = 0

    print(f"{'─'*55}")
    print("  AGENT RUNNING...\n")

    # Step 4: Visit every room in traversal order
    for next_pos in traversal:

        # Move to next room if not already there
        if agent_pos != next_pos:
            agent_pos = move(agent_pos, next_pos)
            steps += 1

        # Sense the current room's cleanliness
        percept = sense(environment, agent_pos)
        print(f"  [SENSE]  Room {agent_pos} is {percept}")

        # Decide action based on percept
        action = agent_decision(percept)

        # Execute action
        if action == "CLEAN":
            clean(environment, agent_pos)
            rooms_cleaned += 1
            steps += 1

        # Brief pause for readability during simulation
        time.sleep(0.3)

    # Step 5: Final environment state
    print(f"\n{'─'*55}")
    print("  FINAL ENVIRONMENT STATE:")
    display_environment(environment, rows, cols, agent_pos)

    # Step 6: Performance report
    all_clean = all(v == CLEAN for v in environment.values())
    total_rooms = rows * cols

    print("=" * 55)
    print("              PERFORMANCE REPORT")
    print("=" * 55)
    print(f"  Total rooms       : {total_rooms}")
    print(f"  Rooms cleaned     : {rooms_cleaned}")
    print(f"  Rooms already clean: {total_rooms - rooms_cleaned}")
    print(f"  Total steps taken : {steps}")
    print(f"  Mission status    : {'✅ SUCCESS — All rooms clean!' if all_clean else '❌ FAILED'}")
    print("=" * 55)


# ── Entry Point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    # Run a 3x3 grid simulation with 70% chance each room starts dirty
    run_vacuum_agent(rows=3, cols=3, dirt_probability=0.7)