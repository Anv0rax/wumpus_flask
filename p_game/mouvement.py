import random
from .const import *

# =========================================================
#
# =========================================================

def random_init(matrix, n_rows=N_ROW, n_cols=N_COL, val=PLAYER) :
    retry = True
    
    while retry :
        row = random.randint(0, n_rows-1)
        col = random.randint(0, n_cols-1)
        
        if val == PLAYER or val == BAT or val == HOLE :
            match matrix[row][col][T_BOX] :
                case 0 : # Normal cavern
                    toReturn = (row, col)
                    retry = False
                case 4 : # Near Hole
                    toReturn = (row, col)
                    retry = False

        elif val == WUMPUS :
            match matrix[row][col][T_BOX] :
                case 0 : # Normal cavern
                    toReturn = (row, col)
                    retry = False
                case 4 : # Near Hole
                    toReturn = (row, col)
                    retry = False
                case 8 : # Hole
                    toReturn = (row, col)
                    retry = False
        else :
            return False
    return toReturn

# =========================================================
#
# =========================================================

def init_player(matrix, n_rows=N_ROW, n_cols=N_COL) :
    pos = random_init(matrix)
    y = pos[0]
    x = pos[1]
    matrix[y][x][T_PLAYER] = IS_HERE
    matrix[y][x][T_VISION] = SEE
    return pos
    
# =========================================================
#
# =========================================================


def move_item(matrix, px, py, mx, my, n_rows=N_ROW, n_cols=N_COL, explorer=False, val=PLAYER) :
    next_x = (px + mx)%n_cols
    next_y = (py + my)%n_rows
    possible = False
    match matrix[py][px][T_BOX] :
        case 1 : # C1                                     →           ↑
            if matrix[py][px][T_PLAYER] == IS_TOP and (mx == 1 or my == -1) :
                possible = make_move_player(matrix, px, py, mx, my, next_x, next_y)

            #                                                ←           ↓
            elif matrix[py][px][T_PLAYER] == IS_BOT and (mx == -1 or my == 1) :
                possible = make_move_player(matrix, px, py, mx, my, next_x, next_y)

        case 2 : # C2                                     ←           ↑
            if matrix[py][px][T_PLAYER] == IS_TOP and (mx == -1 or my == -1) :
                possible = make_move_player(matrix, px, py, mx, my, next_x, next_y)

            #                                                →           ↓
            elif matrix[py][px][T_PLAYER] == IS_BOT and (mx == 1 or my == 1) :
                possible = make_move_player(matrix, px, py, mx, my, next_x, next_y)

        case _ :
            possible = make_move_player(matrix, px, py, mx, my, next_x, next_y)

    if possible :
        if explorer :
            matrix[py][px][T_VISION] = DONT_SEE
        return (possible, next_y, next_x)
    else :
        return(possible, py, px)
    
# =========================================================
#
# =========================================================

def make_move_player(matrix, px, py, mx, my, next_x, next_y) :
    possible = False
    match matrix[next_y][next_x][T_BOX] :
        case 1 : # Corridor 1 = C1
            if mx == 1 : # →
                matrix[next_y][next_x][T_PLAYER] = IS_BOT
                if matrix[next_y][next_x][T_VISION] == DONT_SEE or matrix[next_y][next_x][T_VISION] == SEE_TOP :
                    matrix[next_y][next_x][T_VISION] += SEE_BOT # 10 + -9 == 1 == True
                matrix[py][px][T_PLAYER] = IS_NOT_HERE
                possible = True

            elif mx == -1 : # ←
                if matrix[next_y][next_x][T_VISION] == DONT_SEE or matrix[next_y][next_x][T_VISION] == SEE_BOT :
                    matrix[next_y][next_x][T_VISION] += SEE_TOP # -9 + 10 == 1 == True
                matrix[next_y][next_x][T_PLAYER] = IS_TOP
                matrix[py][px][T_PLAYER] = IS_NOT_HERE
                possible = True

            elif my == 1 : # ↓
                if matrix[next_y][next_x][T_VISION] == DONT_SEE or matrix[next_y][next_x][T_VISION] == SEE_BOT :
                    matrix[next_y][next_x][T_VISION] += SEE_TOP
                matrix[next_y][next_x][T_PLAYER] = IS_TOP
                matrix[py][px][T_PLAYER] = IS_NOT_HERE
                possible = True

            elif my == -1 : # ↑
                if matrix[next_y][next_x][T_VISION] == DONT_SEE or matrix[next_y][next_x][T_VISION] == SEE_TOP :
                    matrix[next_y][next_x][T_VISION] += SEE_BOT
                matrix[next_y][next_x][T_PLAYER] = IS_BOT
                matrix[py][px][T_PLAYER] = IS_NOT_HERE
                possible = True

        case 2 : # Corridor 2 = C2
            if mx == 1 : # →
                matrix[next_y][next_x][T_PLAYER] = IS_TOP
                if matrix[next_y][next_x][T_VISION] == DONT_SEE or matrix[next_y][next_x][T_VISION] == SEE_BOT :
                    matrix[next_y][next_x][T_VISION] += SEE_TOP
                matrix[py][px][T_PLAYER] = IS_NOT_HERE
                possible = True

            elif mx == -1 : # ←
                if matrix[next_y][next_x][T_VISION] == DONT_SEE or matrix[next_y][next_x][T_VISION] == SEE_TOP :
                    matrix[next_y][next_x][T_VISION] += SEE_BOT
                matrix[next_y][next_x][T_PLAYER] = IS_BOT
                matrix[py][px][T_PLAYER] = IS_NOT_HERE
                possible = True

            elif my == 1 : # ↓
                if matrix[next_y][next_x][T_VISION] == DONT_SEE or matrix[next_y][next_x][T_VISION] == SEE_BOT :
                    matrix[next_y][next_x][T_VISION] += SEE_TOP
                matrix[next_y][next_x][T_PLAYER] = IS_TOP
                matrix[py][px][T_PLAYER] = IS_NOT_HERE
                possible = True

            elif my == -1 : # ↑
                if matrix[next_y][next_x][T_VISION] == DONT_SEE or matrix[next_y][next_x][T_VISION] == SEE_TOP :
                    matrix[next_y][next_x][T_VISION] += SEE_BOT
                matrix[next_y][next_x][T_PLAYER] = IS_BOT
                matrix[py][px][T_PLAYER] = IS_NOT_HERE
                possible = True

        case _ :
            matrix[next_y][next_x][T_VISION] = SEE
            matrix[next_y][next_x][T_PLAYER] = IS_HERE
            matrix[py][px][T_PLAYER] = IS_NOT_HERE
            possible = True

    return possible