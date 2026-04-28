from .mouvement import *


def flood_fill_map(matrix, n_rows, n_cols, difficulty) :
    is_map_explorable(matrix, n_rows, n_cols, (0,0))
    if not test_all_map(matrix, n_rows, n_cols) :
        raise Exception("Non valid map")

# =========================================================
# 
# =========================================================
    
def test_all_map(matrix, n_rows, n_cols) :
    row = 0
    col = 0
    playable = True
    while row < n_rows-1:
        col = 1
        while col < n_cols-1 :
            playable *= matrix[row][col][1]
            col = col+1
        row = row+1
    return playable

# =========================================================
# 
# =========================================================

def test_flood_fill(matrix, px, py, mx, my, next_x, next_y) :
    possible = False
    if not matrix[next_y][next_x][1] == True :
        match matrix[next_y][next_x][0] :
            case 1 :
                if matrix[py][px][2] == 1 and (mx == 1 or my == -1) :
                    possible = make_move_player(matrix, px, py, mx, my, next_x, next_y)

                elif matrix[py][px][2] == -1 and (mx == -1 or my == 1) :
                    possible = make_move_player(matrix, px, py, mx, my, next_x, next_y)

            case 2 :
                if matrix[py][px][2] == 1 and (mx == -1 or my == -1) :
                    possible = make_move_player(matrix, px, py, mx, my, next_x, next_y)

                elif matrix[py][px][2] == -1 and (mx == 1 or my == 1) :
                    possible = make_move_player(matrix, px, py, mx, my, next_x, next_y)

            case _ :
                possible = make_move_player(matrix, px, py, mx, my, next_x, next_y)
        if possible :
            return (possible, next_y, next_x)
    return (possible, py, px)

# =========================================================
# 
# =========================================================

def is_map_explorable(matrix, n_rows, n_cols, pos) :
    py, px = pos

    if matrix[py][px][1] :
        return
    
    s_px = px
    s_py = py
    
    n_px = px
    n_py = py
    
    e_px = px
    e_py = py

    w_px = px
    w_py = py

    can_next = True
    while (can_next) :
        (s_can_next, s_py, s_px) = test_flood_fill(matrix, s_px, s_py, 0, +1, s_px, ((s_py+1)%n_rows))
        (n_can_next, n_py, n_px) = test_flood_fill(matrix, n_px, n_py, 0, -1, n_px, ((n_py-1)%n_rows))
        (e_can_next, e_py, e_px) = test_flood_fill(matrix, e_px, e_py, +1, 0, ((e_px+1)%n_cols), e_py)
        (w_can_next, w_py, w_px) = test_flood_fill(matrix, w_px, w_py, -1, 0, ((w_px-1)%n_cols), w_py)
        if s_can_next :
            is_map_explorable(matrix, n_rows, n_cols, (s_py, s_px))
        if n_can_next :
            is_map_explorable(matrix, n_rows, n_cols, (n_py, n_px))
        if e_can_next :
            is_map_explorable(matrix, n_rows, n_cols, (e_py, e_px))
        if w_can_next :
            is_map_explorable(matrix, n_rows, n_cols, (w_py, w_px))
        can_next = s_can_next * n_can_next * e_can_next * w_can_next