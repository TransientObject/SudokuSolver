import time

def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [a+b for a in A for b in B]

digits   = '123456789'
rows     = 'ABCDEFGHI'
cols     = digits
cells    = cross(rows, cols)

# list of units which needs to satisfy the sudoku constraints (all rows + all cols + all subsquares)
sudoku_unit = ([cross(rows, col) for col in cols] +
            [cross(row, cols) for row in rows] +
            [cross(row, col) for row in ('ABC','DEF','GHI') for col in ('123','456','789')])

#dictionary mapping of each cell to the list of units it belongs to
units = dict((cell, [unit for unit in sudoku_unit if cell in unit])
             for cell in cells)

#dictionary mapping of each cell to the list of cells that it should be mutually exclusive with (rows,cols,cells -  20 peers for each cell (8 in the square, 6 in the rows and 6 in the column))
peers = dict((cell, set(sum(units[cell],[]))-set([cell]))
             for cell in cells)

def isGoalFound(possible_values):
    return all([len(value) == 1 for value in possible_values.values()])

def hidden_single_reduction(possible_values):
    assigned_a_new_position = True
    while(assigned_a_new_position):
        assigned_a_new_position = False
        multi_values_cells = sorted([(len(values), cell, values) for cell, values in possible_values.items() if len(values) > 1])
        for multi_values_cell in multi_values_cells:
            values = multi_values_cell[2]
            for value in values:
                if (value in possible_values[multi_values_cell[1]]):
                    for unit in units[multi_values_cell[1]]:
                        peers_which_can_hold_this_values = [cell for cell in unit if value in possible_values[cell]]
                        if(len(peers_which_can_hold_this_values) == 1): # i'm the only one who can hold this value
                            assigned_a_new_position = True
                            possible_values[multi_values_cell[1]] = value
                            possible_values = eliminate_single_values_from_peers(possible_values, [multi_values_cell[1]])

    return possible_values

def solve(start_state):
    possible_values = dict(zip(cells,start_state))
    for cell in cells:
        if (possible_values[cell] == '0'):
            possible_values[cell] = digits

    single_valued_cells = [cell for cell, values in possible_values.items() if len(values) == 1]
    possible_values = eliminate_single_values_from_peers(possible_values, single_valued_cells)
    if (not isGoalFound(possible_values)):
        possible_values = hidden_single_reduction(possible_values)

    goal_state = ''.join(possible_values.values())
    #assert(len(goal_state) == 81)
    return goal_state

def eliminate_single_values_from_peers(possible_values, single_valued_cells):
    new_single_valued_cells = []
    for single_valued_cell in single_valued_cells:
        unique_val = possible_values[single_valued_cell]
        for peer_cell in peers[single_valued_cell]:
            if (len(possible_values[peer_cell]) > 1):
                possible_values[peer_cell] = possible_values[peer_cell].replace(unique_val, '')
                if(len(possible_values[peer_cell]) == 1):
                    #new single_valued cell found. eliminate this value from all the peers
                    single_valued_cells.append(peer_cell)
            assert(len(possible_values[peer_cell]) > 0)
    return possible_values

def display(values):
    print(''.join(list(values.values())))


def display(values):
    i = 1
    line = ""
    for value in values:
        line += value
        if (i % 27 == 0):
            print(line + "\n------------+---------------+------------")
            line = ""
        elif (i % 9 == 0):
            print(line + "\n")
            line =""
        elif(i%3==0):
            line += "   |   "
        else:
            line += "\t"
        i += 1

start = time.time()
start_state = '030500060010030020500069300000000270003704600065000000004320005090050030050008040'
display(solve(start_state))
end = time.time()
print(end - start)

