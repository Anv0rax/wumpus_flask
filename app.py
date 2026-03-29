#!/usr/bin/env python3

from flask import Flask, render_template, redirect, request, session
import random
from werkzeug.security import generate_password_hash, check_password_hash
import psycopg

EASY = 0
NORMAL = 1
HARD = 2

N_ROW = 6
N_COL = 8

def generate_grid(difficulty, n_rows, n_cols) :
    matrix = [[[0, False, False, 0, 0, 0] for _ in range(n_cols) ] for _ in range(n_rows) ]
    match difficulty :
        case 0 :
            choose = [0]*(n_rows*n_cols-8) + [random.choice([1, 2]) for _ in range(14)]
        case 1 :
            choose = [0]*(n_rows*n_cols-18) + [random.choice([1, 2]) for _ in range(24)]
        case 2 :
            choose = [0]*(n_rows*n_cols-28) + [random.choice([1, 2]) for _ in range(34)]

    # North
    col = 0

    while col < n_cols :
        matrix[0][col][0] = choose.pop(random.randint(0, len(choose)-1))
        col = col+1
    
    # West
    row = 0

    while row < n_rows :
        matrix[row][0][0] = choose.pop(random.randint(0, len(choose)-1))
        row = row+1

    # Center
    row = 1

    while row < n_rows-1:
        col = 1
        while col < len(matrix[row])-1 :
            rand = random.randint(0, len(choose)-1)
            while check_nw(matrix, row, col, choose[rand]) :
                rand = random.randint(0, len(choose)-1)

            matrix[row][col][0] = choose.pop(rand)
            col = col+1
        row = row+1

    # East
    row = 1
    col = n_cols-1

    while row < n_rows-1 :
        rand = random.randint(0, len(choose)-1)
        while check_nw(matrix, row, col, choose[rand]) | check_ne(matrix, row, col, choose[rand]) :
            rand = random.randint(0, len(choose)-1)
        matrix[row][col][0] = choose.pop(rand)
        row = row+1

    # South
    row = n_rows-1
    col = 1

    while col < n_cols-1 :
        rand = random.randint(0, len(choose)-1)
        while check_nw(matrix, row, col, choose[rand]) | check_sw(matrix, row, col, choose[rand]) :
            rand = random.randint(0, len(choose)-1)
        matrix[row][col][0] = choose.pop(rand)
        col = col+1

    # Corner
    rand = random.randint(0, len(choose)-1)
    stop_while = 0
    while (check_corner(matrix, n_rows, n_cols, choose[rand])) and stop_while < 5 :
        rand = random.randint(0, len(choose)-1)
        stop_while = stop_while+1
    if stop_while == 5 :
        matrix[row][col][0] = 0
    else :
        matrix[row][col][0] = choose.pop(rand)
    col = col+1

    return matrix

# =============================
#           Check

def check_nw(matrix, row, col, type) :
    retry = False
    if type == 2 :
        if matrix[row-1][col][0] == 1 :
            if matrix[row][col-1][0] == 1 :
                if (matrix[row-1][col-1][0] == 2) :
                    retry = True
    return retry

def check_ne(matrix, row, col, type) :
    retry = False
    if type == 1 :
        if matrix[row-1][col][0] == 2 :
            if matrix[row][0][0] == 2 :
                if (matrix[row-1][0][0] == 1) :
                    retry = True
    return retry

def check_sw(matrix, row, col, type) :
    retry = False
    if type == 1 :
        if matrix[0][col][0] == 2 :
            if matrix[row][col-1][0] == 2 :
                if (matrix[0][col-1][0] == 1) :
                    retry = True
    return retry

def check_se(matrix, row, col, type) :
    retry = False
    if type == 2 :
        if matrix[0][col][0] == 1 :
            if matrix[row][0][0] == 1 :
                if (matrix[0][0][0] == 2) :
                    retry = True
    return retry

def check_corner(matrix, n_rows, n_cols, type) :
    row = n_rows-1
    col = n_cols-1

    retry = False
    match type :
        case 1 :
            retry = check_ne(matrix, row, col, type) | check_sw(matrix, row, col, type)
        case 2 :
            retry = check_nw(matrix, row, col, type) | check_se(matrix, row, col, type)
    return retry

# =============================
#           Play
# ============================= 

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

def init_player(matrix, n_rows, n_cols) :
    pos = random_init(matrix, n_rows, n_cols)
    y = pos[0]
    x = pos[1]
    matrix[y][x][2] = True
    matrix[y][x][1] = True
    return pos

def verify_difficulty(mode) :
    try :
        n = int(mode)
        if not n in [0, 1, 2] :
            n = 1
    except :
        n = 1
    return n

def verify_move(move) :
    try :
        x, y = move
        x = int(x)
        y = int(y)
        return (not x == y and not x == -y) and (x == 1 or x == 0 or x == -1) and (y == 1 or y == 0 or y == -1) 
    except :
        return False

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



# =============================
#           Flask
# =============================

app = Flask(
    __name__,
    template_folder="templates",
    static_folder="static"
)

app.config["SECRET_KEY"] = "a modifer"

@app.errorhandler(404)
def not_found(e):
  return render_template("base.html")

@app.route("/")
def home():
    return redirect("/start")

@app.route("/start")
def start():
    matrix = generate_grid(HARD, N_ROW, N_COL)
    session["map"] = matrix
    session["player"] = init_player(matrix, N_ROW, N_COL)
    return redirect("/play")

@app.route("/play")
def play():
    if session.get("map") and session.get("player") :
        coord = request.args
        x = coord.get('x', type=int, default=0)
        y = coord.get('y', type=int, default=0)
        if verify_move((x,y)) :
            session["player"] = move_item(session["map"], N_ROW, N_COL, session["player"][1], session["player"][0], x, y)
        return render_template("hunt-the-wumpus.html", grid=session["map"])
    else :
        return redirect("/select-difficulty")

@app.route('/select-difficulty', methods=["GET", "POST"])
def select() :
    if request.method == "POST" :
        return redirect("/start")
    else :
        return render_template("select-difficulty.html")

@app.route('/settings')
def settings() :
    return render_template("settings.html")

@app.route('/title-screen')
def title() :
    return render_template("title-screen.html")

@app.route('/stats')
def stats():
    return render_template("stats.html")

@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/menu')
def menu():
    return render_template('menu.html')

if __name__ == '__main__' :
    app.run(debug=True)
