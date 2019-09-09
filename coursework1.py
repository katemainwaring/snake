import time
import copy

import numpy as np

# Load sudokus
#sudokus = np.load("resources/data/sudokus.npy")
#print("Shape of sudokus array:", sudokus.shape, "; Type of array values:", sudokus.dtype)

# Load solutions
#solutions = np.load("resources/data/solutions.npy")
#print("Shape of solutions array:", solutions.shape, "; Type of array values:", solutions.dtype, "\n")

#Print the first sudoku...
#print("Sudoku #1:")
#print(sudokus[14], "\n")

# ...and its solution
#print("Solution of Sudoku #1:")
#print(solutions[14])

#sudokus = np.load("resources/data/sudoku-sample-15-unsolvable.npy")
#sudokus = np.load("resources/data/sudoku-sample-1000.npy")
#Print the first sudoku...
#print("Sudoku #1:")
#print(sudokus[0], "\n")



def find_next_cell_forwards(sudoku, i, j):
    #print("reached 31")
    if i == -1:
        return -1,-1
    for x in range(i,9):
        for y in range(j,9):
            if sudoku[x][y] == 0:
                ##print((x,y))
                return x,y
    return -1,-1

def find_next_cell_backwards(copy_sudoku, sudoku, i, j):
    if i != 0:
        first_time_through = 1
        for x in range(i,-1,-1):
            if first_time_through == 0:
                j = 9
            if j == 0:
                first_time_through = 0
            for y in range(j-1,-1,-1):
                first_time_through = 0
                if copy_sudoku[x][y] == 0:
                    a = sudoku[x][y] + 1
                    for unassigned_no in range(a, 10):
                        if insert_valid_number(sudoku, x, y, unassigned_no):
                            sudoku[x][y] = unassigned_no
                            return x, y
                    sudoku[x][y] = 0

    elif i == 0:
        for y in range(j - 1, -1, -1):
            if copy_sudoku[0][y] == 0:
                a = sudoku[0][y]+1
                for unassigned_no in range(a, 10):
                    if insert_valid_number(sudoku, 0, y, unassigned_no):
                        sudoku[0][y] = unassigned_no
                        return 0, y
                sudoku[0][y] = 0
    return -1,-1

def insert_valid_number(sudoku, i, j, unassigned_no):
    correct_row = all(unassigned_no != sudoku[i][x] for x in range(0,9))
    if correct_row:
        correct_column = all(unassigned_no != sudoku[x][j] for x in range(0,9))
        if correct_column:
        #check 3x3 grid as well here
            a=0
            b=0
            if i>=0 and i<=2:
                a = 0
            if i>=3 and i<=5:
                a = 3
            if i>=6 and i<=8:
                a = 6
            if j>=0 and j<=2:
                b = 0
            if j>=3 and j<=5:
                b = 3
            if j>=6 and j<=8:
                b = 6
            for x in range(a,a+3):
                for y in range(b,b+3):
                    if sudoku[x][y] == unassigned_no:
                        return False
            return True
#call this process first to speed up the algorithm
def insert_initial_values (sudoku):
    changes = 1
    while changes == 1:
        for x in range(0, 9):
            for y in range(0, 9):
                if sudoku[x][y] == 0:
                    for unassigned_no in range(1, 10):
                        if insert_valid_number(sudoku, x, y, unassigned_no):
                            unique_fit = 1
                            for check_number in range (1,10):
                                if check_number != unassigned_no:
                                    if insert_valid_number(sudoku, x, y, check_number):
                                        unique_fit = 0
                            if unique_fit == 1:
                                sudoku[x][y] = unassigned_no
                            else: changes = 0
                        else: changes = 0

def sudoku_solver(sudoku):
    i=0
    insert_initial_values(sudoku)
    copy_sudoku = copy.deepcopy(sudoku)
    while True:
        j=0
        pair = find_next_cell_forwards(sudoku, i, j)
        x = pair[0]
        y = pair[1]
        if x == -1:
            for x in range(0,9):
                for y in range(0,9):
                    if sudoku[x][y] == 0:
                        print(np.full((9,9),-1))
            #print(sudoku)
            return sudoku
            break
        valid = False
        for unassigned_no in range(1,10):
            if insert_valid_number(sudoku, x, y, unassigned_no):
                sudoku[x][y] = unassigned_no
                valid = True
                break
        if not valid:
            sudoku[x][y] = 0
            pair2 = find_next_cell_backwards(copy_sudoku, sudoku, x, y)
            i = pair2[0]
            j = pair2[1]

    return sudoku


sudokuhardish = [
         [8,8,0,0,0,0,0,0,0],
         [0,0,3,6,0,0,0,0,0],
         [0,7,0,0,9,0,2,0,0],
         [0,5,0,0,0,7,0,0,0],
         [0,0,0,0,4,5,7,0,0],
         [0,0,0,1,0,0,0,3,0],
         [0,0,1,0,0,0,0,6,8],
         [0,0,8,5,0,0,0,1,0],
         [0,9,0,0,0,0,4,0,0]
         ]

sudokuveryhard = [
         [0,0,0,0,0,6,0,0,0],
         [0,5,9,0,0,0,0,0,8],
         [2,0,0,0,0,8,0,0,0],
         [0,4,5,0,0,0,0,0,0],
         [0,0,3,0,0,0,0,0,0],
         [0,0,6,0,0,3,0,5,4],
         [0,0,0,3,2,5,0,0,6],
         [0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0]
         ]

sudokutrial = [
         [0,0,0,0,0,0,0,7,0],
         [0,0,0,9,0,1,0,0,6],
         [0,0,9,0,0,5,0,0,8],
         [4,0,0,0,0,0,0,1,3],
         [7,1,0,4,0,6,0,0,0],
         [0,2,0,0,0,0,0,0,0],
         [0,3,0,0,0,0,0,2,0],
         [0,9,8,7,0,2,0,4,0],
         [0,6,0,0,9,0,0,0,0],
         ]
start_time = time.time()

#for i in range(14):
    #print(np.array_equal(sudoku_solver(sudokus[i]), solutions[i]))
print(sudoku_solver(sudokutrial))

print("--- %s seconds ---" % (time.time() - start_time))

