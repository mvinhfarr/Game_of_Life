import numpy as np


class Grid:
    def __init__(self, arr=None):
        if arr is None:
            self.size = self.width, self.height = 1000, 1000
            self.grid = np.zeros(self.size)
        else:
            self.size = self.width, self.height = arr.shape
            self.grid = arr

    def turn(self):
        new_grid = np.zeros(self.size)

        # rules:
        # 1. any live cell with fewer than 2 live neighbours dies
        # 2. any live cells with 2 or 3 live neighbours lives
        # 3. any live cells with more than 3 live neighbours dies
        # 4. any dead cell with 3 live neighbours becomes alive

        for (i, j), cell in np.ndenumerate(self.grid):
            neighbours_idx = (i-1, i-1, i-1, i, i, i+1, i+1, i+1), (j-1, j-1, j-1, j, j, j+1, j+1, j+1)
            neighbours = self.grid[neighbours_idx]
            live_neighbours = np.count_nonzero(neighbours)

            if cell == 1:
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
