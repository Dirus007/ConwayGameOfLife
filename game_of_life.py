# game_of_life.py
import numpy as np

class GameOfLife:
    def __init__(self, width, height, cell_size):
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.grid_width = width // cell_size
        self.grid_height = height // cell_size
        self.grid = np.zeros((self.grid_height, self.grid_width), dtype=bool)

    def update_grid(self):
        new_grid = self.grid.copy()
        for y in range(self.grid_height):
            for x in range(self.grid_width):
                neighbors = sum([self.grid[y + a][x + b] for a in (-1, 0, 1) for b in (-1, 0, 1)
                                 if (a, b) != (0, 0) and 0 <= y + a < self.grid_height and 0 <= x + b < self.grid_width])
                if self.grid[y][x]:
                    if neighbors < 2 or neighbors > 3:
                        new_grid[y][x] = False
                elif neighbors == 3:
                    new_grid[y][x] = True
        self.grid = new_grid

    def toggle_cell(self, x, y):
        self.grid[y][x] = not self.grid[y][x]
