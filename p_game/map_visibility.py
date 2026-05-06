# base , 
# explored , 
# player , 
# elems

from .const import *

def reveal_map(matrix, n_rows=N_ROW, n_cols=N_COL) :
    row = 0
    while row < n_rows :
        col = 0
        while col < n_cols :
            matrix[row][col][T_VISION] = SEE
            col = col+1
        row = row+1


def hide_map(matrix, n_rows=N_ROW, n_cols=N_COL) :
    row = 0
    while row < n_rows :
        col = 0
        while col < n_cols :
            matrix[row][col][T_VISION] = DONT_SEE
            col = col+1
        row = row+1