import math
import time
import sys
import collections

row_col_headers = "123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def chunks(arr,n):
    for i in range(0, len(arr), n):
        yield arr[i:i + n]


class SudokuBase():

    def __init__(self,n):
        self.rows = self.cols = row_col_headers[:n]
        box_size = int(math.sqrt(n))
        self.cells = self.cross(self.rows, self.cols)

        # list of units which needs to satisfy the sudoku constraints (all rows + all cols + all subsquares)
        self.sudoku_units = ([self.cross(self.rows, col) for col in self.cols] +
                            [self.cross(row, self.cols) for row in self.rows] +
                            [self.cross(row, col) for row in chunks(self.rows, box_size) for col in chunks(self.cols, box_size)])

        # dictionary mapping of each cell to the list of units it belongs to
        self.cell_to_units_mapping = dict((cell, [unit for unit in self.sudoku_units if cell in unit])
                                            for cell in self.cells)

        # dictionary mapping of each cell to the list of cells that it should be mutually exclusive with (rows,cols,cells -  20 peers for each cell (8 in the square, 6 in the rows and 6 in the column))
        self.peers = dict((cell, set(sum(self.cell_to_units_mapping[cell], [])) - set([cell]))
                     for cell in self.cells)


    def cross(self,rows,cols):
        return [row+col for row in rows for col in cols]

    def digits(self):
        return self.rows

    def display(self,values):
        i = 1
        line = ""
        for value in values:
            line += value
            if (i % 27 == 0):
                print(line + "\n--------------------+-----------------------+---------------------")
                line = ""
            elif (i % 9 == 0):
                print(line + "\n")
                line = ""
            elif (i % 3 == 0):
                line += "   |   "
            else:
                line += "\t"
            i += 1
