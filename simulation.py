
import pygame
from pathlib import Path
from metrics import save_metrics
import time

ROWS = 18
COLS = 24
CELL_SIZE = 32
WIDTH = COLS * CELL_SIZE
HEIGHT = ROWS * CELL_SIZE

BACKGROUND = (25, 29, 40)
GRID_COLOR = (65, 72, 88)
OBSTACLE_COLOR = (90, 95, 110)
PATH_COLOR = (40, 200, 120)
START_COLOR = (60, 150, 255)
GOAL_COLOR = (255, 75, 75)
ROBOT_COLOR = (255, 210, 50)
TEXT_COLOR = (240, 240, 240)


def create_grid():
    grid = [[0 for _ in range(COLS)] for _ in range(ROWS)]

    # Vertical obstacles with gaps for navigation
    for row in range(ROWS):
        if row != 5:
            grid[row][6] = 1

        if row != 13:
            grid[row][12] = 1

        if row != 8:
            grid[row][18] = 1

    return grid


class NavigationSimulation:
    def __init__(self, grid, path, start, goal):
        pygame.init()
        pygame.display.set_caption("AI-Based Autonomous Navigation System")

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT + 50))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 18)

        self.grid = grid
        self.path = path or []
        self.start = start
        self.goal = goal
        self.robot_index = 0
        self.finished = False
        self.saved = False
        self.started_at = time.perf_counter()

    def draw_cell(self, row, col, color):
        rect = pygame.Rect(
            col * CELL_SIZE,
            row * CELL_SIZE,
            CELL_SIZE,
            CELL_SIZE
        )
        pygame.draw.rect(self.screen, color, rect)
        pygame.draw.rect(self.screen, GRID_COLOR, rect, 1)

    def draw(self):
        self.screen.fill(BACKGROUND)

        path_set = set(self.path)
        robot_position = (
            self.path[min(self.robot_index, len(self.path) - 1)]
            if self.path else self.start
        )

        for row in range(ROWS):
            for col in range(COLS):
                position = (row, col)

                if self.grid[row][col] == 1:
                    color = OBSTACLE_COLOR
                elif position in path_set:
                    color = PATH_COLOR
                else:
                    color = BACKGROUND

                if position == self.start:
                    color = START_COLOR

                if position == self.goal:
                    color = GOAL_COLOR

                if position == robot_position:
                    color = ROBOT_COLOR

                self.draw_cell(row, col, color)

        status = "Destination reached!" if self.finished else "Robot navigating..."
        status_surface = self.font.render(
            f"{status}   |   S: Save screenshot   |   ESC: Exit",
            True,
            TEXT_COLOR
        )
        self.screen.blit(status_surface, (10, HEIGHT + 14))
        pygame.display.flip()

    def save_screenshot(self):
        output_dir = Path("outputs")
        output_dir.mkdir(parents=True, exist_ok=True)
        screenshot_path = output_dir / "navigation_screenshot.png"
        pygame.image.save(self.screen, str(screenshot_path))
        print(f"Screenshot saved to: {screenshot_path}")

    def run(self):
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_s:
                        self.save_screenshot()

            if self.path and not self.finished:
                if self.robot_index < len(self.path) - 1:
                    self.robot_index += 1
                else:
                    self.finished = True

            if self.finished and not self.saved:
                elapsed = time.perf_counter() - self.started_at
                save_metrics(
                    self.path,
                    self.start,
                    self.goal,
                    self.path,
                    "SUCCESS",
                    elapsed
                )
                self.saved = True

            self.draw()
            self.clock.tick(4)

        pygame.quit()
