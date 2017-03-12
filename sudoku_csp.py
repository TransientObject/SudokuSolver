#!/usr/bin/python
import sys
import sudoku_puzzles

def cross(A, B):
    return [a+b for a in A for b in B]

digits   = '123456789'
rows     = 'ABCDEFGHI'
cols     = digits
squares  = cross(rows, cols)
allunits = ([cross(rows, c) for c in cols] +
            [cross(r, cols) for r in rows] +
            [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')])
units = dict((s, [u for u in allunits if s in u])
             for s in squares)
peers = dict((s, set(sum(units[s],[]))-set([s]))
             for s in squares)

def to_grid(puzzle):
    """Read in a puzzle stored as a list and
    transform it into a grid stored as a string."""
    return ''.join(map(str, puzzle))

def init_values(grid):
    """Convert grid which is a string with '0' or '.' for empties into a dictionary
    which specifies the assigned value for that square at the beginning. """
    chars = [c for c in grid if c in digits or c in '0.']
    return dict(zip(squares, chars))

def grid_to_values(grid):
    """Convert grid to values which is a dictionary storing possible digits for
    each square. It returns False if there is contradiction"""
    # We start by assigning each squares the domain {1,2,3,4,5,6,7,8,9}.
    remaining_values = dict((s, digits) for s in squares)
    for s,d in init_values(grid).items():
        if d in digits and not assign(remaining_values, s, d):
            return False
    return remaining_values

def assign(remaining_values, s, d):
    """Eliminate all the other values (except d) from remaining_values[s] and propagate."""
    other_values = remaining_values[s].replace(d, '')
    if all(cons_prop(remaining_values, s, d2) for d2 in other_values):
        return remaining_values
    else:
        return False

def cons_prop(remaining_values, s, d):
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
        if not all(cons_prop(remaining_values, s2, d2) for s2 in peers[s]):
            return False
    # In a unit, if there is only one square for a value, we put the value into this square and do propagation to
    # its peers according to the above strategy.
    for u in units[s]:
        possible_places = [s for s in u if d in remaining_values[s]]
    if len(possible_places) == 0:
        return False
    elif len(possible_places) == 1:
        # d can only be in one place in unit; assign it there
            if not assign(remaining_values, possible_places[0], d):
                return False
    return remaining_values

def display(remaining_values):
    """Display these values as a 2-D grid."""
    width = 1+max(len(remaining_values[s]) for s in squares)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(remaining_values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)

def csp_dfs_search(remaining_values):
    """a search algorithm that combines CSP and DFS"""
    if remaining_values is False:
        return False
    if all(len(remaining_values[s]) == 1 for s in squares):
        return remaining_values
    ## Chose the  square s with the minimum number of possible values
    n,s = min((len(remaining_values[s]), s) for s in squares if len(remaining_values[s]) > 1)

    for d in remaining_values[s]:
        result = csp_dfs_search(assign(remaining_values.copy(), s, d))
        if result:
            return result



def csp_dfs_solve(grid): return csp_dfs_search(grid_to_values(grid))
def csp_solve(grid):
    remaining_values = grid_to_values(grid)

    if all(len(remaining_values[s]) == 1 for s in squares):
        return remaining_values
    else:
        print("The puzzle can't be solved using only current CSP strategies.")


# if __name__=="__main__":
#     puzzles = dict()
#     for i in dir(sudoku_puzzles):
#         if '__' not in i:
#             puzzles[i] = getattr(sudoku_puzzles, i)

#     if len(sys.argv) <= 1:
#         print("Please use the following flag to call the corresponding solver: ")
#         print("   -- a: Search ")
#         print("   -- b: Pure CSP ")
#         print("   -- c: CSP + Search ")
#     elif sys.argv[1] == 'b':
#         for puzzle in puzzles:
#             result = csp_solve(to_grid(puzzles[puzzle]))
#             display(result)
#     elif sys.argv[1] == 'c':
#         for puzzle in puzzles:
#             result = csp_dfs_solve(to_grid(puzzles[puzzle]))
#             display(result)
