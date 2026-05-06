import random
from .const import *

# =========================================================
# 
# =========================================================

def generate_grid(difficulty, n_rows=N_ROW, n_cols=N_COL) :
    # box , vision , player , elem
    matrix = [[[0, False, False, 0] for _ in range(n_cols) ] for _ in range(n_rows) ]
    len_choose = 53
    match difficulty :
        case 0 :
            choose = [0]*40 + [random.choice([1, 2]) for _ in range(14)]
        case 1 :
            choose = [0]*30 + [random.choice([1, 2]) for _ in range(24)]
        case 2 :
            choose = [0]*20 + [random.choice([1, 2]) for _ in range(34)]

    # North
    col = 0

    while col < n_cols :
        matrix[0][col][T_BOX] = choose.pop(random.randint(0, len_choose))
        len_choose -= 1
        col = col+1
    
    # West
    row = 0

    while row < n_rows :
        matrix[row][0][T_BOX] = choose.pop(random.randint(0, len_choose))
        len_choose -= 1
        row = row+1

    # Center
    row = 1

    while row < n_rows-1:
        col = 1
        while col < n_cols-1 :
            rand = random.randint(0, len_choose)
            while check_nw(matrix, row, col, choose[rand]) :
                rand = random.randint(0, len_choose)
            matrix[row][col][T_BOX] = choose.pop(rand)
            len_choose -= 1
            col = col+1
        row = row+1

    # East
    row = 1
    col = n_cols-1

    while row < n_rows-1 :
        rand = random.randint(0, len_choose)
        while check_nw(matrix, row, col, choose[rand]) | check_ne(matrix, row, col, choose[rand]) :
            rand = random.randint(0, len_choose)
        matrix[row][col][T_BOX] = choose.pop(rand)
        len_choose -= 1
        row = row+1

    # South
    row = n_rows-1
    col = 1

    while col < n_cols-1 :
        rand = random.randint(0, len_choose)
        while check_nw(matrix, row, col, choose[rand]) | check_sw(matrix, row, col, choose[rand]) :
            rand = random.randint(0, len_choose)
        matrix[row][col][T_BOX] = choose.pop(rand)
        len_choose -= 1
        col = col+1

    # Corner
    rand = random.randint(0, len_choose)
    stop_while = 0
    while (check_corner(matrix, choose[rand])) and stop_while < 5 :
        rand = random.randint(0, len_choose)
        stop_while = stop_while+1
    if stop_while == 5 :
        matrix[row][col][T_BOX] = 0
    else :
        matrix[row][col][T_BOX] = choose.pop(rand)
    len_choose -= 1
    col = col+1
    
    return matrix


# =========================================================
# 
# =========================================================


# =============================
#           Check

def check_nw(matrix, row, col, type) :
    retry = False
    if type == C2 :
        if matrix[row-1][col][T_BOX] == C1 :
            if matrix[row][col-1][T_BOX] == C1 :
                if (matrix[row-1][col-1][T_BOX] == C2) :
                    retry = True
    return retry

def check_ne(matrix, row, col, type) :
    retry = False
    if type == C1 :
        if matrix[row-1][col][T_BOX] == C2 :
            if matrix[row][0][T_BOX] == C2 :
                if (matrix[row-1][0][T_BOX] == C1) :
                    retry = True
    return retry

def check_sw(matrix, row, col, type) :
    retry = False
    if type == C1 :
        if matrix[0][col][T_BOX] == C2 :
            if matrix[row][col-1][T_BOX] == C2 :
                if (matrix[0][col-1][T_BOX] == C1) :
                    retry = True
    return retry

def check_se(matrix, row, col, type) :
    retry = False
    if type == C2 :
        if matrix[0][col][T_BOX] == C1 :
            if matrix[row][0][T_BOX] == C1 :
                if (matrix[0][0][T_BOX] == C2) :
                    retry = True
    return retry

def check_corner(matrix, type, n_rows=N_ROW, n_cols=N_COL) :
    row = n_rows-1
    col = n_cols-1

    retry = False
    match type :
        case 1 : # C1
            retry = check_ne(matrix, row, col, type) | check_sw(matrix, row, col, type)
        case 2 : # C2
            retry = check_nw(matrix, row, col, type) | check_se(matrix, row, col, type)
    return retry