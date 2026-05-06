from .const import *
from .mouvement import move_item, follow_corridor

def check_player(matrix, player) :
    y, x = player

    result = 1

    if matrix[y][x][T_ELEMS] == WUMPUS :
        result = -2

    elif matrix[y][x][T_BOX] == HOLE :
        result = -3

    elif matrix[y][x][T_ELEMS] in (BAT, BAT+N_WUMP) :
        matrix[y][x][T_ELEMS] += ADD_TRIG_BAT
        result = 2

    elif matrix[y][x][T_ELEMS] in (TRIG_BAT, TRIG_BAT+N_WUMP) :
        result = 3

    return result

# =========================================================
#
# =========================================================

def shoot_arrow(matrix, player, my, mx) :
    py, px = player

    touched = -4

    (possible, next_y, next_x) = move_item(matrix, py, px, my, mx)
    if not matrix[next_y][next_x][T_BOX] in (CAVERN, N_HOLE, HOLE) :
        next_y, next_x = follow_corridor(matrix, next_y, next_x, my, mx)
    
    if matrix[next_y][next_x][T_BOX] in (CAVERN, N_HOLE, HOLE) :
        matrix[next_y][next_x][T_VISION] = 4
        touched = -1 if matrix[next_y][next_x][T_ELEMS] == WUMPUS else -4
    
    matrix[next_y][next_x][T_PLAYER] = IS_NOT_HERE

    return touched