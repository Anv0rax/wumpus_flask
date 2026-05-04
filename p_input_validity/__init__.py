# __init__.py

def verify_move(move) :
    try :
        y, x = move
        y = int(y)
        x = int(x)
        return (not x == y and not x == -y) and (x == 1 or x == 0 or x == -1) and (y == 1 or y == 0 or y == -1) 
    except :
        return False