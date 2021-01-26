import numpy as np


class Grid:
    def __init__(self, shape=(100, 100), arr=None, edge_strat='toroidal'):
        # self.strats = ['toroidal', 'finite', 'finite+1']
        self.strats = ['toroidal', 'finite']
        if edge_strat not in self.strats:
            raise ValueError('Invalid edge stratege. Expected one of %s' % self.strats)
        self.edge_strat = edge_strat

        if arr is not None:
            self.size = self.width, self.height = arr.shape
            self.grid = arr
        else:
            self.size = self.width, self.height = shape
            self.grid = np.zeros((self.width, self.height), dtype=np.bool_)

    #     self.border = self.build_border()
    #
    # def build_border(self):
    #     border = {}
    #     ''
    #
    #     return border

    def get_neighbours(self, i, j):
        neighbours_idx = (i-1, i-1, i-1, i,   i,   i+1, i+1, i+1),\
                         (j-1, j,   j+1, j-1, j+1, j-1, j,   j+1)

        if self.edge_strat == 'toroidal':
            if (i == self.height-1) | (j == self.height-1):
                filtered_i = tuple(ni if ni < self.height else ni - self.height for ni in neighbours_idx[0])
                filtered_j = tuple(nj if nj < self.height else nj - self.height for nj in neighbours_idx[1])
                neighbours_idx = filtered_i, filtered_j
        else:
            if (i == 0) | (i == self.height - 1) | (j == 0) | (j == self.width - 1):
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

    # def fill_random(self, density, spread=None):
