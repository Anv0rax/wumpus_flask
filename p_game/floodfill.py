from .mouvement import *
from .const import *

def flood_fill_map(matrix) :
    pos = init_player(matrix)
    ff_exploring(matrix, pos, 0, +1)
    ff_exploring(matrix, pos, 0, -1)
    ff_exploring(matrix, pos, +1, 0)
    ff_exploring(matrix, pos, -1, 0)
    return test_all_map_and_hide(matrix)

# =========================================================
# 
# =========================================================

def ff_exploring(matrix, pos, mx, my, n_rows=N_ROW, n_cols=N_COL) :
    py, px = pos

    next_x = (px + mx)%n_cols
    next_y = (py + my)%n_rows

    if matrix[next_y][next_x][T_VISION] == True :
        return
    elif matrix[next_y][next_x][T_BOX] == C1 :
        #    →           ↑
        if (mx == 1 or my == -1) and matrix[next_y][next_x][T_VISION] == SEE_BOT :
            return
        #    ←           ↓
        if (mx == -1 or my == 1) and matrix[next_y][next_x][T_VISION] == SEE_TOP :
            return
        
    elif matrix[next_y][next_x][T_BOX] == C2 :
        #    ←           ↑
        if (mx == -1 or my == -1) and matrix[next_y][next_x][T_VISION] == SEE_BOT :
            return
        #    →          ↓
        if (mx == 1 or my == 1) and matrix[next_y][next_x][T_VISION] == SEE_TOP :
            return

    (possible, now_y, now_x) = move_item(matrix, px, py, mx, my)

    if possible :
        ff_exploring(matrix, (now_y, now_x), 0, +1)
        ff_exploring(matrix, (now_y, now_x), 0, -1)
        ff_exploring(matrix, (now_y, now_x), +1, 0)
        ff_exploring(matrix, (now_y, now_x), -1, 0)
    return

# =========================================================
# 
# =========================================================
    
def test_all_map_and_hide(matrix, n_rows=N_ROW, n_cols=N_COL) :
    row = 0
    playable = True
    while row < n_rows and playable :
        col = 0
        while col < n_cols and playable :
            playable *= matrix[row][col][T_VISION] == 1
            matrix[row][col][T_VISION] = DONT_SEE
            matrix[row][col][T_PLAYER] = IS_NOT_HERE
            col = col+1
        row = row+1
    return playable