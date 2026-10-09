
import time
from planner import find_path
from simulation import create_grid, NavigationSimulation


def main():
    grid = create_grid()

    start = (1, 1)
    goal = (16, 22)

    print("AI-Based Autonomous Navigation System")
    print("-------------------------------------")
    print(f"Start position: {start}")
    print(f"Goal position: {goal}")
    print("Planning path using A* algorithm...")

    start_time = time.perf_counter()
    path = find_path(grid, start, goal)
    elapsed_time = time.perf_counter() - start_time

    if path is None:
        print("No valid path found!")
        return

    print("Path found successfully!")
    print(f"Path cells: {len(path)}")
    print(f"Number of steps: {len(path) - 1}")
    print(f"Planning time: {elapsed_time:.6f} seconds")
    print("Opening robot simulation...")

    simulation = NavigationSimulation(grid, path, start, goal)
    simulation.run()


if __name__ == "__main__":
    main()
