"""
============================================================
  DEPTH-FIRST SEARCH (DFS)
============================================================
  - Uses a STACK (Last In, First Out)
  - Dives as deep as possible before backtracking
  - Does NOT guarantee the shortest path
  - Time Complexity : O(V + E)
  - Space Complexity: O(V)

  Two versions provided:
    1. Iterative DFS  — explicit stack (safe for large graphs)
    2. Recursive DFS  — uses Python's call stack (cleaner)
============================================================
"""


# Graph represented as an adjacency list.
# Same graph as bfs.py for easy comparison.
GRAPH = {
    'A': ['B', 'C'],
    'B': ['A', 'D', 'E'],
    'C': ['A', 'F'],
    'D': ['B'],
    'E': ['B', 'F'],
    'F': ['C', 'E', 'G'],
    'G': ['F']
}


# ============================================================
#  VERSION 1 — ITERATIVE DFS
# ============================================================

def dfs_iterative(graph, start, goal):
    """
    Iterative DFS using an explicit stack.

    The stack holds full PATHS (lists of nodes).
    list.pop() removes from the RIGHT end = LIFO order.
    This is the only structural difference from BFS,
    which uses queue.popleft() (FIFO).
    """

    if start == goal:
        print(f"Start node '{start}' is already the goal.")
        return [start]

    # Stack holds PATHS, not just individual nodes
    stack = [[start]]

    # Visited set prevents cycles
    visited = set()
    visited.add(start)

    print(f"\n{'='*52}")
    print(f"  DFS (Iterative)  |  Start: '{start}'   Goal: '{goal}'")
    print(f"{'='*52}")
    print(f"  {'Step':<6} {'Exploring':<14} Stack (upcoming nodes)")
    print(f"  {'-'*46}")

    step = 0

    while stack:
        step += 1

        # Pop the NEWEST path — LIFO, so it dives deep first
        current_path = stack.pop()
        current_node = current_path[-1]

        stack_preview = [p[-1] for p in stack]
        print(f"  {step:<6} {current_node:<14} {stack_preview}")

        # Goal check on the node just popped
        if current_node == goal:
            print(f"\n  Goal '{goal}' reached!\n")
            return current_path

        # Push unvisited neighbours onto the stack
        for neighbour in graph.get(current_node, []):
            if neighbour in visited:
                continue
            visited.add(neighbour)
            stack.append(current_path + [neighbour])

    print(f"\n  No path found from '{start}' to '{goal}'.\n")
    return None


# ============================================================
#  VERSION 2 — RECURSIVE DFS
# ============================================================

def dfs_recursive(graph, current, goal,
                  visited=None, path=None, step_counter=None):
    """
    Recursive DFS — Python's own call stack acts as the DFS stack.

    Parameters
    ----------
    graph        : adjacency list dictionary
    current      : node currently being explored
    goal         : target node to find
    visited      : shared set of already-explored nodes
    path         : current path from start to `current`
    step_counter : single-element list used as a shared integer
                   counter across recursive calls
    """

    # Initialise mutable defaults on the very first call only
    if visited is None:      visited = set()
    if path is None:         path = []
    if step_counter is None: step_counter = [0]

    # Mark current node as visited and extend the path
    visited.add(current)
    path = path + [current]     # creates a new list — safe across calls

    step_counter[0] += 1
    print(f"  {step_counter[0]:<6} {current:<14} {' -> '.join(path)}")

    # Base case: we reached the goal
    if current == goal:
        return path

    # Recursive case: explore each unvisited neighbour
    for neighbour in graph.get(current, []):
        if neighbour not in visited:
            result = dfs_recursive(graph, neighbour, goal,
                                   visited, path, step_counter)
            if result is not None:
                return result       # propagate the found path upward

    # Backtrack: no path found from this node
    return None


# ── Entry point — runs both versions ─────────────────────
if __name__ == "__main__":
    START = 'A'
    GOAL  = 'G'

    # --- Iterative DFS ---
    path_iter = dfs_iterative(GRAPH, START, GOAL)
    if path_iter:
        print(f"  Search path : {' -> '.join(path_iter)}")
        print(f"  Path length : {len(path_iter) - 1} edge(s)")
    print(f"{'='*52}\n")

    # --- Recursive DFS ---
    print(f"\n{'='*52}")
    print(f"  DFS (Recursive)  |  Start: '{START}'   Goal: '{GOAL}'")
    print(f"{'='*52}")
    print(f"  {'Step':<6} {'Exploring':<14} Path so far")
    print(f"  {'-'*46}")

    path_rec = dfs_recursive(GRAPH, START, GOAL)

    if path_rec:
        print(f"\n  Goal '{GOAL}' reached!\n")
        print(f"  Search path : {' -> '.join(path_rec)}")
        print(f"  Path length : {len(path_rec) - 1} edge(s)")
    else:
        print(f"\n  No path found.\n")
    print(f"{'='*52}\n")