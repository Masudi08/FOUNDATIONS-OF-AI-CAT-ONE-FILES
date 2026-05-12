import heapq

def astar(grid, start, goal):
    rows, cols = len(grid), len(grid[0])

    # Heuristic: Manhattan distance
    def h(node):
        return abs(node[0] - goal[0]) + abs(node[1] - goal[1])

    # Priority queue: (f(n), node)
    open_list = []
    heapq.heappush(open_list, (0, start))

    # Track costs and parents
    g = {start: 0}
    parent = {start: None}

    while open_list:
        _, current = heapq.heappop(open_list)

        # Goal reached
        if current == goal:
            path = []
            while current:
                path.append(current)
                current = parent[current]
            path.reverse()
            return path

        # Explore neighbors (Up, Down, Left, Right)
        for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
            neighbor = (current[0]+dx, current[1]+dy)
            nr, nc = neighbor

            # Skip out-of-bounds or blocked cells
            if not (0 <= nr < rows and 0 <= nc < cols):
                continue
            if grid[nr][nc] == 1:  # 1 = obstacle
                continue

            new_g = g[current] + 1

            if neighbor not in g or new_g < g[neighbor]:
                g[neighbor] = new_g
                f = new_g + h(neighbor)
                heapq.heappush(open_list, (f, neighbor))
                parent[neighbor] = current

    return None  # No path found


# --- Grid Setup ---
# 0 = free cell, 1 = obstacle
grid = [
    [0, 0, 0, 0, 0],
    [0, 1, 1, 1, 0],
    [0, 0, 0, 1, 0],
    [0, 1, 0, 0, 0],
    [0, 0, 0, 0, 0],
]

start = (0, 0)  # Top-left
goal  = (4, 4)  # Bottom-right

path = astar(grid, start, goal)

# --- Output ---
if path:
    print(f"Optimal path found ({len(path)-1} steps):")
    for step in path:
        print(f"  -> {step}")

    # Visualize on grid
    print("\nGrid (S=Start, G=Goal, * =Path, X=Obstacle):")
    for r in range(len(grid)):
        row = ""
        for c in range(len(grid[0])):
            if (r, c) == start:
                row += " S"
            elif (r, c) == goal:
                row += " G"
            elif (r, c) in path:
                row += " *"
            elif grid[r][c] == 1:
                row += " X"
            else:
                row += " ."
        print(row)
else:
    print("No path found.")