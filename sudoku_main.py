from sudoku_csp import *
from sudoku_csp_optimized import *
from sudoku_backtracking import *


def solve_sudoku(method, start_state):
    if (method == 'a'):
        sudoku = SudokuBackTracking(int(math.sqrt(len(start_state))), start_state)
        if (sudoku.solve_sudoku()):
            sudoku.display(''.join(sudoku.possible_values.values()))
        else:
            print("No solution exists")
    elif(method == 'b'):
        sudoku = SudokuCSPOptimized(int(math.sqrt(len(start_state))), start_state)
        goal = sudoku.solve(start_state)
        if (goal):
            sudoku.display(goal)
        else:
            print("The puzzle can't be solved using only current CSP strategies.")
            return -1
    elif(method == 'c'):
        sudoku = SudokuCSP(int(math.sqrt(len(start_state))))
        result = sudoku.csp_solve(start_state)
        if result:
            goal = (collections.OrderedDict(sorted(result.items()))).values()
            sudoku.display(goal)
        else:
            print("The puzzle can't be solved using only current CSP strategies.")
            return -1
    elif(method == 'd'):
        sudoku = SudokuCSP(int(math.sqrt(len(start_state))))
        result = sudoku.csp_dfs_solve(start_state)
        goal = (collections.OrderedDict(sorted(result.items()))).values()
        sudoku.display(goal)
    else:
        print("invalid algorithm choice. Enter a/b/c")
        exit(0)

    return 0


# if __name__=="__main__":
#     if(len(sys.argv) < 3):
#         print("invalid format - To run, execute sudoku_base.py [a|b|c] <sudoku_puzzle>")
#         exit(0)
#
#     start_state = sys.argv[2]
#     sqt = math.sqrt(math.sqrt(len(start_state)))
#     if(sqt != int(sqt)):
#         print("sudoku input is incorrect. should be a perfect n ^ 4")
#         exit(0)
#
#     solve_sudoku(sys.argv[1], start_state)