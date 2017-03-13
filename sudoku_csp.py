from sudoku_base import *

class SudokuCSP(SudokuBase):
    def __init__(self,n):
        SudokuBase.__init__(self,n)

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
        elif len(remaining_values[s]) == 2:
            for u in self.cell_to_units_mapping[s]:
                d2 = remaining_values[s]
                possible_twins = [s for s in u if remaining_values[s] == d2]
                if len(possible_twins) >= 2:
                    other_squares_this_unit = [s for s in u if not s in possible_twins]
                    for char in d2:
                        if not all(self.cons_prop(remaining_values, s2, char) for s2 in other_squares_this_unit):
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
            return False