# base , 
# explored , 
# player , 
# elem

def reveal_map(matrix, n_rows, n_cols) :
    row = 0
    col = 0
    while row < n_rows-1:
        col = 1
        while col < n_cols-1 :
            matrix[row][col][1] = True
            col = col+1
        row = row+1


def hide_map(matrix, n_rows, n_cols) :
    row = 0
    col = 0
    while row < n_rows-1:
        col = 1
        while col < n_cols-1 :
            matrix[row][col][1] = False
            col = col+1
        row = row+1