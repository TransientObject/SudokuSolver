from sudoku_base import *
from memory_profiler import profile

class SudokuBackTracking(SudokuBase):
    def __init__(self,n, start_state):
        SudokuBase.__init__(self,n)
        self.possible_values = dict(zip(self.cells,start_state))


    def find_empty_location(self):
        for cell in self.cells:
            if(self.possible_values[cell] == '0'):
                return cell
        return False


    def check_location_is_safe(self, empty_cell, num):
        for peer_cell in self.peers[empty_cell]:
            if (self.possible_values[peer_cell] == num):
                return False
        return True

    def solve_sudoku(self):
        empty_cell = self.find_empty_location()
        if (empty_cell is False):
            return True

        for num in range(1, 10):
            if (self.check_location_is_safe(empty_cell, str(num))):
                self.possible_values[empty_cell] = str(num)
                if (self.solve_sudoku()):
                    return True
                self.possible_values[empty_cell] = '0'

        return False
