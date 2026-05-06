from .const import *
    
# =========================================================
#
# =========================================================

def verify_move(move) :
    try :
        y, x = move
        y = int(y)
        x = int(x)
        return (not x == y and not x == -y) \
           and (x == 1 or x == 0 or x == -1) \
           and (y == 1 or y == 0 or y == -1) 
    except :
        return False
    
# =========================================================
#
# =========================================================

def move_item(matrix, py, px, my, mx, n_rows=N_ROW, n_cols=N_COL, blind=False, val=PLAYER) :
    next_y = (py + my)%n_rows
    next_x = (px + mx)%n_cols
    possible = False
    match matrix[py][px][T_BOX] :
        case 1 : # C1                                     →           ↑
            if matrix[py][px][T_PLAYER] == IS_TOP and (mx == 1 or my == -1) :
                possible = make_move_player(matrix, py, px, my, mx, next_y, next_x)

            #                                                ←           ↓
            elif matrix[py][px][T_PLAYER] == IS_BOT and (mx == -1 or my == 1) :
                possible = make_move_player(matrix, py, px, my, mx, next_y, next_x)

        case 2 : # C2                                     ←           ↑
            if matrix[py][px][T_PLAYER] == IS_TOP and (mx == -1 or my == -1) :
                possible = make_move_player(matrix, py, px, my, mx, next_y, next_x)

            #                                                →           ↓
            elif matrix[py][px][T_PLAYER] == IS_BOT and (mx == 1 or my == 1) :
                possible = make_move_player(matrix, py, px, my, mx, next_y, next_x)

        case _ :
            possible = make_move_player(matrix, py, px, my, mx, next_y, next_x)

    if possible :
        if blind :
            matrix[py][px][T_VISION] = DONT_SEE
        return (possible, next_y, next_x)
    else :
        return(possible, py, px)
    
# =========================================================
#
# =========================================================

def make_move_player(matrix, py, px, my, mx, next_y, next_x) :
    moved = False
    match matrix[next_y][next_x][T_BOX] :
        case 1 : # Corridor 1 = C1
            if mx == 1 : # →
                matrix[next_y][next_x][T_PLAYER] = IS_BOT
                if matrix[next_y][next_x][T_VISION] == DONT_SEE \
                  or matrix[next_y][next_x][T_VISION] == SEE_TOP :
                    matrix[next_y][next_x][T_VISION] += SEE_BOT # 10 + -9 == 1 == True
                
                matrix[py][px][T_PLAYER] = IS_NOT_HERE
                moved = True

            elif mx == -1 : # ←
                if matrix[next_y][next_x][T_VISION] == DONT_SEE \
                  or matrix[next_y][next_x][T_VISION] == SEE_BOT :
                    matrix[next_y][next_x][T_VISION] += SEE_TOP # -9 + 10 == 1 == True
                
                matrix[next_y][next_x][T_PLAYER] = IS_TOP
                matrix[py][px][T_PLAYER] = IS_NOT_HERE
                moved = True

            elif my == 1 : # ↓
                if matrix[next_y][next_x][T_VISION] == DONT_SEE \
                  or matrix[next_y][next_x][T_VISION] == SEE_BOT :
                    matrix[next_y][next_x][T_VISION] += SEE_TOP
                
                matrix[next_y][next_x][T_PLAYER] = IS_TOP
                matrix[py][px][T_PLAYER] = IS_NOT_HERE
                moved = True

            elif my == -1 : # ↑
                if matrix[next_y][next_x][T_VISION] == DONT_SEE \
                  or matrix[next_y][next_x][T_VISION] == SEE_TOP :
                    matrix[next_y][next_x][T_VISION] += SEE_BOT
                
                matrix[next_y][next_x][T_PLAYER] = IS_BOT
                matrix[py][px][T_PLAYER] = IS_NOT_HERE
                moved = True

        case 2 : # Corridor 2 = C2
            if mx == 1 : # →
                matrix[next_y][next_x][T_PLAYER] = IS_TOP
                if matrix[next_y][next_x][T_VISION] == DONT_SEE \
                  or matrix[next_y][next_x][T_VISION] == SEE_BOT :
                    matrix[next_y][next_x][T_VISION] += SEE_TOP
                
                matrix[py][px][T_PLAYER] = IS_NOT_HERE
                moved = True

            elif mx == -1 : # ←
                if matrix[next_y][next_x][T_VISION] == DONT_SEE \
                  or matrix[next_y][next_x][T_VISION] == SEE_TOP :
                    matrix[next_y][next_x][T_VISION] += SEE_BOT
                
                matrix[next_y][next_x][T_PLAYER] = IS_BOT
                matrix[py][px][T_PLAYER] = IS_NOT_HERE
                moved = True

            elif my == 1 : # ↓
                if matrix[next_y][next_x][T_VISION] == DONT_SEE \
                  or matrix[next_y][next_x][T_VISION] == SEE_BOT :
                    matrix[next_y][next_x][T_VISION] += SEE_TOP
                
                matrix[next_y][next_x][T_PLAYER] = IS_TOP
                matrix[py][px][T_PLAYER] = IS_NOT_HERE
                moved = True

            elif my == -1 : # ↑
                if matrix[next_y][next_x][T_VISION] == DONT_SEE \
                  or matrix[next_y][next_x][T_VISION] == SEE_TOP :
                    matrix[next_y][next_x][T_VISION] += SEE_BOT
                
                matrix[next_y][next_x][T_PLAYER] = IS_BOT
                matrix[py][px][T_PLAYER] = IS_NOT_HERE
                moved = True

        case _ :
            matrix[next_y][next_x][T_VISION] = SEE
            matrix[next_y][next_x][T_PLAYER] = IS_HERE
            matrix[py][px][T_PLAYER] = IS_NOT_HERE
            moved = True

    return moved
    
# =========================================================
#
# =========================================================

def follow_corridor(matrix, y, x, my, mx, blind=False, n_rows=N_ROW, n_cols=N_COL, condition=(CAVERN, N_HOLE, HOLE)) :
    while matrix[y][x][T_BOX] not in condition :
        # Si c2 bas : si mx = -1 alors faut faire my -1
        # Ou + 1 → +1
        #C1 faut inverse x et y et tu suis le chemin

        # C2 si c'est x-1 → y+1 donc swap négatif

        match matrix[y][x][T_BOX] :
            case 1 : # C1
                temp = mx
                mx = my
                my = temp
            case 2 : # C2
                temp = -mx
                mx = -my
                my = temp
        (possible, y, x) = move_item(matrix, y, x, my, mx, blind=blind)
    
    return (y, x)