from .const import *

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
