import math
import time
import sys

row_col_headers = "123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def chunks(arr,n):
    for i in range(0, len(arr), n):
        yield arr[i:i + n]


class SudokuMain():

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
                print(line + "\n------------+---------------+------------")
                line = ""
            elif (i % 9 == 0):
                print(line + "\n")
                line = ""
            elif (i % 3 == 0):
                line += "   |   "
            else:
                line += "\t"
            i += 1

class SudokuCSPOptimized(SudokuMain):

    def __init__(self,n):
        SudokuMain.__init__(self,n)

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


# region CSP

class SudokuCSP(SudokuMain):
    def __init__(self,n):
        SudokuMain.__init__(self,n)

    def to_grid(self,puzzle):
        """Read in a puzzle stored as a list and
        transform it into a grid stored as a string."""
        return ''.join(map(str, puzzle))

    def init_values(self,grid):
        """Convert grid which is a string with '0' or '.' for empties into a dictionary
        which specifies the assigned value for that square at the beginning. """
        chars = [c for c in grid if c in self.digits() or c in '0.']
        return dict(zip(self.cells, chars))

    def grid_to_values(self,grid):
        """Convert grid to values which is a dictionary storing possible digits for
        each square. It returns False if there is contradiction"""
        # We start by assigning each self.cells the domain {1,2,3,4,5,6,7,8,9}.
        remaining_values = dict((s, self.digits()) for s in self.cells)
        for s,d in self.init_values(grid).items():
            if d in self.digits() and not self.assign(remaining_values, s, d):
                return False
        return remaining_values

    def assign(self,remaining_values, s, d):
        """Eliminate all the other values (except d) from remaining_values[s] and propagate."""
        other_values = remaining_values[s].replace(d, '')
        if all(self.cons_prop(remaining_values, s, d2) for d2 in other_values):
            return remaining_values
        else:
            return False

    def cons_prop(self,remaining_values, s, d):
        """This function does constraint propagation."""
        if d not in remaining_values[s]:
            return remaining_values # no propagation needed
        remaining_values[s] = remaining_values[s].replace(d,'')
        # If the possible values of a square has been reduced to one, we eliminate that value from its peers'
        # remaining values.
        if len(remaining_values[s]) == 0:
            return False
        elif len(remaining_values[s]) == 1:
            d2 = remaining_values[s]
            if not all(self.cons_prop(remaining_values, s2, d2) for s2 in self.peers[s]):
                return False
        # In a unit, if there is only one square for a value, we put the value into this square and do propagation to
        # its peers according to the above strategy.
        for u in self.cell_to_units_mapping[s]:
            possible_places = [s for s in u if d in remaining_values[s]]
        if len(possible_places) == 0:
            return False
        elif len(possible_places) == 1:
            # d can only be in one place in unit; assign it there
                if not self.assign(remaining_values, possible_places[0], d):
                    return False
        return remaining_values

    def csp_dfs_search(self,remaining_values):
        """a search algorithm that combines CSP and DFS"""
        if remaining_values is False:
            return False
        if all(len(remaining_values[s]) == 1 for s in self.cells):
            return remaining_values
        ## Chose the  square s with the minimum number of possible values
        n,s = min((len(remaining_values[s]), s) for s in self.cells if len(remaining_values[s]) > 1)

        for d in remaining_values[s]:
            result = self.csp_dfs_search(self.assign(remaining_values.copy(), s, d))
            if result:
                return result

    def csp_dfs_solve(self,grid):
        return self.csp_dfs_search(self.grid_to_values(grid))

    def csp_solve(self,grid):
        remaining_values = self.grid_to_values(grid)

        if all(len(remaining_values[s]) == 1 for s in self.cells):
            return remaining_values
        else:
            print("The puzzle can't be solved using only current CSP strategies.")

# end region CSP

if __name__=="__main__":
    if(len(sys.argv) < 3):
        print("invalid format - To run, execute sudoku_main.py [a|b|c] <sudoku_puzzle>")

    start_state = sys.argv[2]
    sqt = math.sqrt(math.sqrt(len(start_state)))
    if(sqt != int(sqt)):
        print("sudoku input is incorrect. should be a perfect n ^ 4")
        exit(0)

    if (sys.argv[1] == 'a'):
        sudoku = SudokuCSPOptimized(int(math.sqrt(len(start_state))))
        goal = sudoku.solve(sys.argv[2])
        print(goal)
        sudoku.display(goal)
    elif(sys.argv[1] == 'b'):
        sudoku = SudokuCSP(int(math.sqrt(len(start_state))))
        goal = sudoku.csp_solve(sys.argv[2])
        print(goal)
        sudoku.display(goal)
    elif(sys.argv[1] == 'c'):
        sudoku = SudokuCSP(int(math.sqrt(len(start_state))))
        goal = sudoku.csp_dfs_solve(sys.argv[2])
        print(goal)
        sudoku.display(goal)
    else:
        print("invalid algorithm choice. Enter a/b/c")