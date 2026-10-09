
import heapq


def heuristic(current, goal):
    return abs(current[0] - goal[0]) + abs(current[1] - goal[1])


def find_path(grid, start, goal):
    if not grid or not grid[0]:
        raise ValueError("Grid cannot be empty")

    rows = len(grid)
    cols = len(grid[0])

    if any(len(row) != cols for row in grid):
        raise ValueError("Grid must be rectangular")

    def is_valid(position):
        row, col = position
        return 0 <= row < rows and 0 <= col < cols

    if not is_valid(start) or not is_valid(goal):
        raise ValueError("Start and goal must be inside the grid")

    if grid[start[0]][start[1]] == 1:
        raise ValueError("Start position is blocked")

    if grid[goal[0]][goal[1]] == 1:
        raise ValueError("Goal position is blocked")

    open_list = []
    heapq.heappush(
        open_list,
        (heuristic(start, goal), 0, start)
    )

    came_from = {}
    g_score = {start: 0}
    visited = set()

    directions = [
        (-1, 0),
        (1, 0),
        (0, -1),
        (0, 1)
    ]

    while open_list:
        _, current_cost, current = heapq.heappop(open_list)

        if current in visited:
            continue

        visited.add(current)

        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]

            path.append(start)
            path.reverse()
            return path

        for dr, dc in directions:
            neighbor = (current[0] + dr, current[1] + dc)

            if not is_valid(neighbor):
                continue

            row, col = neighbor

            if grid[row][col] == 1:
                continue

            new_cost = current_cost + 1

            if new_cost < g_score.get(neighbor, float("inf")):
                g_score[neighbor] = new_cost
                came_from[neighbor] = current

                estimated_cost = new_cost + heuristic(neighbor, goal)

                heapq.heappush(
                    open_list,
                    (estimated_cost, new_cost, neighbor)
                )

    return None
