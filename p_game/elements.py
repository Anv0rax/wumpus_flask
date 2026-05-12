import random
from .const import *
from .mouvement import move_item, follow_corridor

# =========================================================
#
# =========================================================

def random_init(matrix, n_rows=N_ROW, n_cols=N_COL, val=PLAYER) :
    retry = True
    
    while retry :
        row = random.randint(0, n_rows-1)
        col = random.randint(0, n_cols-1)
        
        match val :
            case 0 : # First init player
                if ( matrix[row][col][T_ELEMS] == 0 ) \
                 and ( matrix[row][col][T_BOX] == CAVERN ) :
                    toReturn = (row, col)
                    retry = False

            case 32 : # WUMPUS
                if matrix[row][col][T_BOX] in (CAVERN, N_HOLE, HOLE) :
                    toReturn = (row, col)
                    retry = False

            case 8 : # HOLE
                if matrix[row][col][T_BOX] in (CAVERN, N_HOLE) :
                    toReturn = (row, col)
                    retry = False

            case i if i == PLAYER or i == BAT :
                if ( matrix[row][col][T_ELEMS] in (0, N_WUMP) ) \
                 and ( matrix[row][col][T_BOX] in (CAVERN, N_HOLE) ) :
                    toReturn = (row, col)
                    retry = False

            case _ :
                return False
    return toReturn

# =========================================================
#
# =========================================================

def init_player(matrix, n_rows=N_ROW, n_cols=N_COL, first_init=False) :
    if first_init :
        pos = random_init(matrix, val=0)
    else :
        pos = random_init(matrix, val=PLAYER)
    y = pos[0]
    x = pos[1]
    matrix[y][x][T_PLAYER] = IS_HERE
    matrix[y][x][T_VISION] = SEE
    return pos

# =========================================================
#
# =========================================================

def init_bat(matrix, player, wumpus, bat=None) :
    pos = random_init(matrix, val=BAT)
    while pos not in (player, wumpus, bat) :
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

        (possible, next_y, next_x) = move_item(matrix, y, x, my, mx)
        if matrix[next_y][next_x][T_BOX] in (CAVERN, N_HOLE) :
            matrix[next_y][next_x][T_BOX] = N_HOLE
        else :
            next_y, next_x = follow_corridor(matrix, next_y, next_x, my, mx)
            if matrix[next_y][next_x][T_BOX] == CAVERN :
                matrix[next_y][next_x][T_BOX] = N_HOLE
        
        matrix[next_y][next_x][T_PLAYER] = IS_NOT_HERE

# =========================================================
#
# =========================================================

def generate_around(matrix, pos, type=N_WUMP, wump=False) :
    y, x = pos
    move = ((-1, 0), (1, 0), (0, 1), (0, -1))

    if type == N_WUMP :
        tab = T_ELEMS
    elif type == N_HOLE :
        tab = T_BOX
        matrix[y][x][T_BOX] = HOLE

    for direction in range(4) :
        my , mx = move[direction%4]

        (possible, next_y, next_x) = move_item(matrix, y, x, my, mx)

        if (next_y, next_x) == wump : # if the wumpus is here, continue
            matrix[next_y][next_x][T_PLAYER] = IS_NOT_HERE
            continue

        if matrix[next_y][next_x][T_BOX] in (CAVERN, N_HOLE) :
            matrix[next_y][next_x][tab] = type
        else :
            next_y, next_x = follow_corridor(matrix, next_y, next_x, my, mx)
            if matrix[next_y][next_x][T_BOX] in (CAVERN, N_HOLE) :

                if (next_y, next_x) == wump : # if the wumpus is here, continue
                    matrix[next_y][next_x][T_PLAYER] = IS_NOT_HERE
                    continue

                matrix[next_y][next_x][tab] = type
        
        matrix[next_y][next_x][T_PLAYER] = IS_NOT_HERE

        if type == N_WUMP and not wump :
            generate_around(matrix, (next_y, next_x), wump=pos, type=N_WUMP)
            matrix[pos[0]][pos[1]][T_ELEMS] = WUMPUS