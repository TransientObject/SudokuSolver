from sudoku_base import *
from collections import *

class SudokuCSPOptimized(SudokuBase):

    def __init__(self, n, start_state):
        SudokuBase.__init__(self,n)
        self.possible_values = dict(zip(self.cells,start_state))

    def isValidGrid(self):
        for unit in self.sudoku_units:
            count = Counter()
            for cell in unit:
                count[self.possible_values[cell]] += 1
                if(all([val == 1 for val in count.values()])):
                    continue
                else:
                    return False
        return True

    def isGoalFound(self):
        if(all([len(value) == 1 for value in self.possible_values.values()])):
            return self.isValidGrid()

    def hidden_single_reduction(self):
        assigned_a_new_position = True
        while(assigned_a_new_position):
            assigned_a_new_position = False
            multi_values_cells = sorted([(len(values), cell, values) for cell, values in self.possible_values.items() if len(values) > 1])
            for multi_values_cell in multi_values_cells:
                values = multi_values_cell[2]
                for value in values:
                    if (value in self.possible_values[multi_values_cell[1]]):
                        for unit in self.cell_to_units_mapping[multi_values_cell[1]]:
                            peers_which_can_hold_this_values = [cell for cell in unit if value in self.possible_values[cell]]
                            if(len(peers_which_can_hold_this_values) == 1): # i'm the only one who can hold this value
                                assigned_a_new_position = True
                                self.possible_values[multi_values_cell[1]] = value
                                self.eliminate_single_values_from_peers([multi_values_cell[1]])

        return self.isGoalFound()

    def solve(self, start_state):
        for cell in self.cells:
            if (self.possible_values[cell] == '0'):
                self.possible_values[cell] = self.digits()

        if(self.solve_helper()):
            goal_state = ''.join(self.possible_values.values())
            return goal_state
        else:
            return False


    def solve_helper(self):
        single_valued_cells = [cell for cell, values in self.possible_values.items() if len(values) == 1]
        if(self.eliminate_single_values_from_peers(single_valued_cells)):
            return True

        if(self.hidden_single_reduction()):
            return True

        return False

    # def dfs_solve(self):
    #     if (self.isGoalFound()):
    #         return True
    #     n, cell = min((len(self.possible_values[cell]), cell) for cell in self.cells if len(self.possible_values[cell]) > 1)
    #
    #     temp_possible_values = self.possible_values
    #     for val in temp_possible_values[cell]:
    #         self.possible_values[cell] = val
    #         if (self.solve_helper()):
    #             return True
    #
    #     self.possible_values = temp_possible_values
    #     return False


    def eliminate_single_values_from_peers(self, single_valued_cells):
        new_single_valued_cells = []
        for single_valued_cell in single_valued_cells:
            unique_val = self.possible_values[single_valued_cell]
            for peer_cell in self.peers[single_valued_cell]:
                if (len(self.possible_values[peer_cell]) > 1):
                    self.possible_values[peer_cell] = self.possible_values[peer_cell].replace(unique_val, '')
                    if(len(self.possible_values[peer_cell]) == 1):
                        #new single_valued cell found. eliminate this value from all the peers
                        single_valued_cells.append(peer_cell)
                if(len(self.possible_values[peer_cell]) <= 0):
                    return False
        return self.isGoalFound()