from sudoku_csp import *
from sudoku_csp_optimized import *

if __name__=="__main__":
    if(len(sys.argv) < 3):
        print("invalid format - To run, execute sudoku_base.py [a|b|c] <sudoku_puzzle>")
        exit(0)

    start_state = sys.argv[2]
    sqt = math.sqrt(math.sqrt(len(start_state)))
    if(sqt != int(sqt)):
        print("sudoku input is incorrect. should be a perfect n ^ 4")
        exit(0)

    if (sys.argv[1] == 'a'):
        sudoku = SudokuCSPOptimized(int(math.sqrt(len(start_state))))
        goal = sudoku.solve(sys.argv[2])
        sudoku.display(goal)
    elif(sys.argv[1] == 'b'):
        sudoku = SudokuCSP(int(math.sqrt(len(start_state))))
        result = sudoku.csp_solve(sys.argv[2])
        if result:
            goal = (collections.OrderedDict(sorted(result.items()))).values()
            print(goal)
            sudoku.display(goal)
        else:
            print("The puzzle can't be solved using only current CSP strategies.")
    elif(sys.argv[1] == 'c'):
        sudoku = SudokuCSP(int(math.sqrt(len(start_state))))
        result = sudoku.csp_dfs_solve(sys.argv[2])
        goal = (collections.OrderedDict(sorted(result.items()))).values()
        print(goal)
        sudoku.display(goal)
    else:
        print("invalid algorithm choice. Enter a/b/c")
        exit(0)