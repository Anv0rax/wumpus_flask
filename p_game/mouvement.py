import random

# =========================================================
#
# =========================================================

def random_init(matrix, n_rows, n_cols, val=128) :
    retry = True
    
    while retry :
        row = random.randint(0, n_rows-1)
        col = random.randint(0, n_cols-1)
        
        if val == 128 or val == 64 or val == 8 :
            match matrix[row][col][0] :
                case 0 :
                    toReturn = (row, col)
                    retry = False
                case 4 :
                    toReturn = (row, col)
                    retry = False

        elif val == 32 :
            match matrix[row][col][0] :
                case 0 :
                    toReturn = (row, col)
                    retry = False
                case 4 :
                    toReturn = (row, col)
                    retry = False
                case 8 :
                    toReturn = (row, col)
                    retry = False
        else :
            return False
    return toReturn

# =========================================================
#
# =========================================================

def init_player(matrix, n_rows, n_cols) :
    pos = random_init(matrix, n_rows, n_cols)
    y = pos[0]
    x = pos[1]
    matrix[y][x][2] = True
    matrix[y][x][1] = True
    return pos
    
# =========================================================
#
# =========================================================


def move_item(matrix, n_rows, n_cols, px, py, mx, my, sub=2, explorer=False, val=128) :
    next_x = (px+mx)%n_cols
    next_y = (py+my)%n_rows
    possible = False
    match matrix[py][px][0] :
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
        if explorer :
            matrix[py][px][1] = False
        return (next_y, next_x)
    else :
        return(py, px)
    
# =========================================================
#
# =========================================================

def make_move_player(matrix, px, py, mx, my, next_x, next_y, val=-1) :
    possible = False
    match matrix[next_y][next_x][0] :
        case 1 :
            if mx == 1 :
                matrix[next_y][next_x][2] = -1
                if matrix[next_y][next_x][1] == 0 or matrix[next_y][next_x][1] == 10 : # if we don't see the hole box, see bot
                    matrix[next_y][next_x][1] += -9 # 10 + -9 == 1 == True
                matrix[py][px][2] = False
                possible = True
            elif mx == -1 :
                if matrix[next_y][next_x][1] == 0 or matrix[next_y][next_x][1] == -9 :
                    matrix[next_y][next_x][1] += 10 # -9 + 10 == 1 == True
                matrix[next_y][next_x][2] = 1
                matrix[py][px][2] = False
                possible = True
            elif my == 1 :
                if matrix[next_y][next_x][1] == 0 or matrix[next_y][next_x][1] == -9 :
                    matrix[next_y][next_x][1] += 10
                matrix[next_y][next_x][2] = 1
                matrix[py][px][2] = False
                possible = True
            elif my == -1 :
                if matrix[next_y][next_x][1] == 0 or matrix[next_y][next_x][1] == 10 :
                    matrix[next_y][next_x][1] += -9
                matrix[next_y][next_x][2] = -1
                matrix[py][px][2] = False
                possible = True
        case 2 :
            if mx == 1 :
                matrix[next_y][next_x][2] = 1
                if matrix[next_y][next_x][1] == 0 or matrix[next_y][next_x][1] == -9 :
                    matrix[next_y][next_x][1] += 10
                matrix[py][px][2] = False
                possible = True
            elif mx == -1 :
                if matrix[next_y][next_x][1] == 0 or matrix[next_y][next_x][1] == 10 :
                    matrix[next_y][next_x][1] += -9
                matrix[next_y][next_x][2] = -1
                matrix[py][px][2] = False
                possible = True
            elif my == 1 :
                if matrix[next_y][next_x][1] == 0 or matrix[next_y][next_x][1] == -9 :
                    matrix[next_y][next_x][1] += 10
                matrix[next_y][next_x][2] = 1
                matrix[py][px][2] = False
                possible = True
            elif my == -1 :
                if matrix[next_y][next_x][1] == 0 or matrix[next_y][next_x][1] == 10 :
                    matrix[next_y][next_x][1] += -9
                matrix[next_y][next_x][2] = -1
                matrix[py][px][2] = False
                possible = True
        case _ :
            matrix[next_y][next_x][1] = True
            matrix[next_y][next_x][2] = True
            matrix[py][px][2] = False
            possible = True
    return possible