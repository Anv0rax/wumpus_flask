import random
from .const import *
from .mouvement import *

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
    pos = random_init(matrix, val=PLAYER)
    y = pos[0]
    x = pos[1]
    matrix[y][x][T_PLAYER] = IS_HERE
    matrix[y][x][T_VISION] = SEE
    return pos

# =========================================================
#
# =========================================================

def init_bat(matrix, player, wumpus, hole_1, hole_2, bat=None) :
    pos = random_init(matrix, val=BAT)
    while pos not in (player, wumpus, hole_1, hole_2, bat) :
        pos = random_init(matrix, val=BAT)
    return pos

# =========================================================
#
# =========================================================

def generate_around_hole(matrix, hole) :
    y, x = hole
    move = ((-1, 0), (1, 0), (0, 1), (0, -1))

    matrix[y][x][T_BOX] = HOLE

    for direction in range(4) :
        my , mx = move[direction%4]

        (possible, next_y, next_x) = move_item(matrix, x, y, mx, my)
        if matrix[next_y][next_x][T_BOX] in (CAVERN, N_HOLE) :
            matrix[next_y][next_x][T_BOX] = N_HOLE
        else :
            next_y, next_x = follow_corridor(matrix, x, y, my, mx)
            # matrix[next_y][next_x][T_BOX] = N_HOLE

    return