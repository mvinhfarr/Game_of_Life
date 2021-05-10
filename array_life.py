import random
import numpy as np


class Board:
    """
    Board class represents the game of life field as an NxM array of cells that are either alive (1) or dead (0).
    Because it is a finite array, I have to handle what happens to cells on the edge. Thus, there are two edge
    strategies, toroidal and finite. Toroidal stitches the top and bottom and the left and right sides together. In
    other words, a cell on the top most row has 5 normal neighbors and 3 neighbors on the bottom most row vertically
    aligned. In the corners the same principle applies and for example, the cell in the top right corner checks the
    cell in the bottom left corner. The finite edge strategy simply assumes that all cells outside of the bounds of
    the array are dead. While simpler, this results in some strange behavior on the edge.
    """

    def __init__(self, shape=(100, 100), arr=None, edge_strat='toroidal'):
        """
        Default params creates and empty board of size 100x100 with edge_strat toroidal.

        :param shape: specify the size of the board array if no array is provided
        :param arr: provide a boolean numpy array to be the initial board
        :param edge_strat: specify the strategy to handle cells on the edge
        """

        if arr is not None:  # If an array is provided set it as the grid
            if isinstance(arr, np.ndarray) and arr.dtype == np.bool_:  # Check the provided arr is of valid type
                self.size = self.height, self.width = arr.shape
                self.grid = arr
        else:  # Otherwise initialize the array to be empty, i.e. all zeros
            self.size = self.height, self.width = shape
            self.grid = np.zeros((self.height, self.width), dtype=np.bool_)

        self.strats = ['toroidal', 'finite']
        if edge_strat not in self.strats:  # Check that provided edge_strat is a valid one
            raise ValueError('Invalid edge strategy. Expected one of %s' % self.strats)
        self.edge_strat = edge_strat

    def get_neighbours(self, row, col):
        """
        Returns the 8 or fewer neighbors of a given cell based on the edge strategy.

        :param row: int row
        :param col: int column
        :return: numpy array of neighbor cells
        """

        # Index of neighboring cells -- 8 including diagonals
        neighbours_idx = (row - 1, row - 1, row - 1, row, row, row + 1, row + 1, row + 1), \
                         (col - 1, col, col + 1, col - 1, col + 1, col - 1, col, col + 1)

        # Handle cases when the cell is on the edge
        if self.edge_strat == 'toroidal':
            # We only need to check bottom and right edges as negative indices automatically wrap
            if (row == self.height - 1) | (col == self.width - 1):
                filtered_rows = tuple(ni if ni < self.height else ni - self.height for ni in neighbours_idx[0])
                filtered_cols = tuple(nj if nj < self.width else nj - self.width for nj in neighbours_idx[1])
                neighbours_idx = filtered_rows, filtered_cols
        elif self.edge_strat == 'finite':
            # In a finite board however we have to check all edges
            if (row == 0) | (row == self.height - 1) | (col == 0) | (col == self.width - 1):
                filtered_idx = tuple((ni, nj) for ni, nj in zip(neighbours_idx[0], neighbours_idx[1])
                                     if (ni >= 0) & (nj >= 0) & (ni < self.height) & (nj < self.width))
                neighbours_idx = tuple(zip(*filtered_idx))  # The * argument unpacks the (row, col) tuples

        # Return a Numpy array of the neighbors
        neighbours = self.grid[neighbours_idx]
        return neighbours

    def turn(self):
        """
        Complete one turn following the rules of The Game of Life
        and update all cells in place.

        :return: None
        """
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
        """
        Flip the state of a cell from alive to dead or vice-versa.

        :param row: int row
        :param col: int col
        :return: None
        """

        self.grid[row, col] = 0 if self.grid[row, col] else 1

    def reset_grid(self):
        """
        Clear the board to be all dead

        :return: None
        """

        self.grid = np.zeros(self.size, dtype=np.bool_)

    def set_edge_strat(self, strat):
        """
        Select a different edge strategy from the built-in options.

        :param strat: String - must be one of the provided strats
        :return: None
        """

        if strat not in self.strats:
            raise ValueError('Invalid edge strategy. Expected one of %s' % self.strats)
        self.edge_strat = strat

    def set_grid(self, arr):
        """
        Overwrite the board with the provided one. Provided board can be of any size.

        :param arr: NumPy array of dtype np.bool_
        :return: None
        """

        if isinstance(arr, np.ndarray) and arr.dtype == np.bool_:
            self.grid = arr
            self.size = self.height, self. width = arr.shape

    def fill_random(self, count, spread=None):
        """
        Select a random set of cells and swap their state.
        Spread represents a rectangle around the center of
        where cells can be selected from.

        :param count: int of number of cells to fill
        :param spread: tuple of rows then columns
        :return: None
        """
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

        try:
            rand_rows = random.sample(range(fill_rows[0], fill_rows[1]), count)
            rand_cols = random.sample(range(fill_cols[0], fill_cols[1]), count)
        except ValueError:
            # count is greater than the number of cells in the area of spread
            k1 = fill_rows[1] - fill_rows[0]
            k2 = fill_cols[1] - fill_cols[0]
            rand_rows = random.sample(range(fill_rows[0], fill_rows[1]), k1)
            rand_cols = random.sample(range(fill_cols[0], fill_cols[1]), k2)

        for r, c in zip(rand_rows, rand_cols):
            self.swap_cell_state(r, c)
