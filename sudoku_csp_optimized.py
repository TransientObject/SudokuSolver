from sudoku_base import *

class SudokuCSPOptimized(SudokuBase):

    def __init__(self,n):
        SudokuBase.__init__(self,n)

    def isGoalFound(self, possible_values):
        return all([len(value) == 1 for value in possible_values.values()])

    def hidden_single_reduction(self, possible_values):
        assigned_a_new_position = True
        while(assigned_a_new_position):
            assigned_a_new_position = False
            multi_values_cells = sorted([(len(values), cell, values) for cell, values in possible_values.items() if len(values) > 1])
            for multi_values_cell in multi_values_cells:
                values = multi_values_cell[2]
                for value in values:
                    if (value in possible_values[multi_values_cell[1]]):
                        for unit in self.cell_to_units_mapping[multi_values_cell[1]]:
                            peers_which_can_hold_this_values = [cell for cell in unit if value in possible_values[cell]]
                            if(len(peers_which_can_hold_this_values) == 1): # i'm the only one who can hold this value
                                assigned_a_new_position = True
                                possible_values[multi_values_cell[1]] = value
                                possible_values = self.eliminate_single_values_from_peers(possible_values, [multi_values_cell[1]])

        return possible_values

    def solve(self, start_state):
        possible_values = dict(zip(self.cells,start_state))
        for cell in self.cells:
            if (possible_values[cell] == '0'):
                possible_values[cell] = self.digits()

        single_valued_cells = [cell for cell, values in possible_values.items() if len(values) == 1]
        possible_values = self.eliminate_single_values_from_peers(possible_values, single_valued_cells)
        if (not self.isGoalFound(possible_values)):
            possible_values = self.hidden_single_reduction(possible_values)

        goal_state = ''.join(possible_values.values())
        return goal_state

    def eliminate_single_values_from_peers(self, possible_values, single_valued_cells):
        new_single_valued_cells = []
        for single_valued_cell in single_valued_cells:
            unique_val = possible_values[single_valued_cell]
            for peer_cell in self.peers[single_valued_cell]:
                if (len(possible_values[peer_cell]) > 1):
                    possible_values[peer_cell] = possible_values[peer_cell].replace(unique_val, '')
                    if(len(possible_values[peer_cell]) == 1):
                        #new single_valued cell found. eliminate this value from all the peers
                        single_valued_cells.append(peer_cell)
                assert(len(possible_values[peer_cell]) > 0)
        return possible_values