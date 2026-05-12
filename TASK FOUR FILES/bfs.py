"""
============================================================
  BREADTH-FIRST SEARCH (BFS)
============================================================
  - Uses a QUEUE (First In, First Out)
  - Explores nodes level by level
  - Guarantees the SHORTEST path in an unweighted graph
  - Time Complexity : O(V + E)
  - Space Complexity: O(V)
============================================================
"""

from collections import deque   # deque gives O(1) popleft()


# Graph represented as an adjacency list.
# Each key is a node; its value is the list of neighbours.
GRAPH = {
    'A': ['B', 'C'],
    'B': ['A', 'D', 'E'],
    'C': ['A', 'F'],
    'D': ['B'],
    'E': ['B', 'F'],
    'F': ['C', 'E', 'G'],
    'G': ['F']
}


def bfs(graph, start, goal):
    """
    Perform Breadth-First Search from start to goal.

    Each queue entry is a full PATH (list of nodes) so we
    can reconstruct the route once the goal is found.
    """

    # Edge case: already at the goal
    if start == goal:
        print(f"Start node '{start}' is already the goal.")
        return [start]

    # Queue holds PATHS, not just individual nodes
    queue = deque([[start]])

    # Visited set prevents revisiting nodes (avoids cycles)
    visited = set()
    visited.add(start)

    print(f"\n{'='*52}")
    print(f"  BFS  |  Start: '{start}'   Goal: '{goal}'")
    print(f"{'='*52}")
    print(f"  {'Step':<6} {'Exploring':<14} Queue (upcoming nodes)")
    print(f"  {'-'*46}")

    step = 0

    while queue:
        step += 1

        # Dequeue the OLDEST path — FIFO order
        current_path = queue.popleft()
        current_node = current_path[-1]

        # Show tips of remaining queued paths
        queue_preview = [p[-1] for p in queue]
        print(f"  {step:<6} {current_node:<14} {queue_preview}")

        # Expand all neighbours of the current node
        for neighbour in graph.get(current_node, []):

            if neighbour in visited:
                continue                        # skip already-visited nodes

            new_path = current_path + [neighbour]

            # Goal check before enqueueing (early exit)
            if neighbour == goal:
                print(f"\n  Goal '{goal}' reached!\n")
                return new_path

            visited.add(neighbour)
            queue.append(new_path)

    print(f"\n  No path found from '{start}' to '{goal}'.\n")
    return None


# ── Entry point ──────────────────────────────────────────
if __name__ == "__main__":
    START = 'A'
    GOAL  = 'G'

    path = bfs(GRAPH, START, GOAL)

    if path:
        print(f"  Search path : {' -> '.join(path)}")
        print(f"  Path length : {len(path) - 1} edge(s)")
    print(f"{'='*52}\n")