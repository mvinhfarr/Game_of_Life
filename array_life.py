import random
import numpy as np


class Board:
    def __init__(self, shape=(100, 100), arr=None, edge_strat='toroidal'):
        # self.strats = ['toroidal', 'finite', 'finite+1']
        self.strats = ['toroidal', 'finite']
        if edge_strat not in self.strats:
            raise ValueError('Invalid edge stratege. Expected one of %s' % self.strats)
        self.edge_strat = edge_strat

        if arr is not None:
            self.size = self.height, self.width = arr.shape
            self.grid = arr
        else:
            self.size = self.height, self.width = shape
            self.grid = np.zeros((self.height, self.width), dtype=np.bool_)

    def get_neighbours(self, row, col):
        neighbours_idx = (row - 1, row - 1, row - 1, row, row, row + 1, row + 1, row + 1),\
                         (col - 1, col, col + 1, col - 1, col + 1, col - 1, col, col + 1)

        if self.edge_strat == 'toroidal':
            if (row == self.height - 1) | (col == self.width - 1):
                filtered_rows = tuple(ni if ni < self.height else ni - self.height for ni in neighbours_idx[0])
                filtered_cols = tuple(nj if nj < self.width else nj - self.width for nj in neighbours_idx[1])
                neighbours_idx = filtered_rows, filtered_cols
        else:
            if (row == 0) | (row == self.height - 1) | (col == 0) | (col == self.width - 1):
                filtered_idx = tuple((ni, nj) for ni, nj in zip(neighbours_idx[0], neighbours_idx[1])
                                     if (ni >= 0) & (nj >= 0) & (ni < self.height) & (nj < self.width))
                neighbours_idx = tuple(zip(*filtered_idx))

        neighbours = self.grid[neighbours_idx]
        return neighbours

    def turn(self):
        new_grid = np.zeros(self.size, dtype=np.bool_)

        # rules:
        # 1. any live cell with fewer than 2 live neighbours dies
        # 2. any live cells with 2 or 3 live neighbours lives
        # 3. any live cells with more than 3 live neighbours dies
        # 4. any dead cell with 3 live neighbours becomes alive

        for (i, j), cell in np.ndenumerate(self.grid):
            neighbours = self.get_neighbours(i, j)
            live_neighbours = np.count_nonzero(neighbours)

            if cell:
                if (live_neighbours == 2) or (live_neighbours == 3):  # rule 2
                    new_grid[i, j] = 1
                else:  # rule 1 & 3
                    new_grid[i, j] = 0
            else:
                if live_neighbours == 3:  # rule 4
                    new_grid[i, j] = 1
                else:
                    new_grid[i, j] = 0

        self.grid = new_grid

    def swap_cell_state(self, row, col):
        self.grid[row, col] = 0 if self.grid[row, col] else 1

    def reset_grid(self):
        self.grid = np.zeros(self.size, dtype=np.bool_)

    def set_edge_strat(self, strat):
        if strat not in self.strats:
            raise ValueError('Invalid edge stratege. Expected one of %s' % self.strats)
        self.edge_strat = strat

    def fill_random(self, count, spread=None):
        if spread is None:
            fill_rows = 0, self.height
            fill_cols = 0, self.width
        elif isinstance(spread, tuple) and len(spread) == 2:
            center = self.height // 2, self.width // 2
            half_spread = spread[0] // 2, spread[1] // 2
            fill_rows = center[0] - half_spread[0], center[0] + half_spread[0]
            fill_cols = center[1] - half_spread[1], center[1] + half_spread[1]
        else:
            raise ValueError('Invalid spread. Expected tuple of length 2 (range_rows, range_cols)')

        rand_rows = random.sample(range(fill_rows[0], fill_rows[1]), count)
        rand_cols = random.sample(range(fill_cols[0], fill_cols[1]), count)

        for r, c in zip(rand_rows, rand_cols):
            self.swap_cell_state(r, c)
