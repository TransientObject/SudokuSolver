from sudoku_csp import *
from sudoku_csp_optimized import *
from sudoku_backtracking import *


def solve(method, start_state):
    if (method == 'a'):
        sudoku = SudokuBackTracking(int(math.sqrt(len(start_state))), start_state)
        if (sudoku.solve_sudoku()):
            sudoku.display(''.join(sudoku.possible_values.values()))
        else:
            print("No solution exists")
    elif(method == 'b'):
        sudoku = SudokuCSPOptimized(int(math.sqrt(len(start_state))), start_state)
        goal = sudoku.solve(sys.argv[2])
        if (goal):
            sudoku.display(goal)
        else:
            print("The puzzle can't be solved using only current CSP strategies.")
    elif(method == 'c'):
        sudoku = SudokuCSP(int(math.sqrt(len(start_state))))
        result = sudoku.csp_solve(sys.argv[2])
        if result:
            goal = (collections.OrderedDict(sorted(result.items()))).values()
            print(goal)
            sudoku.display(goal)
        else:
            print("The puzzle can't be solved using only current CSP strategies.")
    elif(method == 'd'):
        sudoku = SudokuCSP(int(math.sqrt(len(start_state))))
        result = sudoku.csp_dfs_solve(sys.argv[2])
        goal = (collections.OrderedDict(sorted(result.items()))).values()
        print(goal)
        sudoku.display(goal)
    else:
        print("invalid algorithm choice. Enter a/b/c")
        exit(0)


if __name__=="__main__":
    if(len(sys.argv) < 3):
        print("invalid format - To run, execute sudoku_base.py [a|b|c] <sudoku_puzzle>")
        exit(0)

    start_state = sys.argv[2]
    sqt = math.sqrt(math.sqrt(len(start_state)))
    if(sqt != int(sqt)):
        print("sudoku input is incorrect. should be a perfect n ^ 4")
        exit(0)

    solve(sys.argv[1], start_state)