import unittest
from planner import find_path


class TestPathPlanner(unittest.TestCase):

    def test_empty_grid(self):
        grid = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        path = find_path(grid, (0, 0), (2, 2))

        self.assertIsNotNone(path)
        self.assertEqual(path[0], (0, 0))
        self.assertEqual(path[-1], (2, 2))
        self.assertEqual(len(path) - 1, 4)

    def test_avoids_obstacle(self):
        grid = [[0, 0, 0], [0, 1, 0], [0, 0, 0]]
        path = find_path(grid, (0, 0), (2, 2))

        self.assertIsNotNone(path)
        for row, col in path:
            self.assertEqual(grid[row][col], 0)

    def test_no_path(self):
        grid = [[0, 1, 0], [0, 1, 0], [0, 1, 0]]
        path = find_path(grid, (0, 0), (0, 2))

        self.assertFalse(path)

    def test_blocked_start(self):
        grid = [[1, 0], [0, 0]]

        with self.assertRaises(ValueError):
            find_path(grid, (0, 0), (1, 1))


if __name__ == "__main__":
    unittest.main()