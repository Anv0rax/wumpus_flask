#!/usr/bin/env python3

from flask import Flask, render_template
import random
#from markupsafe import Markup

EASY = 0
NORMAL = 1
HARD = 2

N_ROW = 6
N_COL = 8



def generate_grid(difficulty, n_rows, n_cols) :
    matrix = [[[0, True, True, 0, 0, 0] for _ in range(n_cols) ] for _ in range(n_rows) ]
    match difficulty :
        case 0 :
            choose = [0]*40 + [random.choice([1, 2]) for _ in range(14)]
        case 1 :
            choose = [0]*30 + [random.choice([1, 2]) for _ in range(24)]
        case 2 :
            choose = [0]*20 + [random.choice([1, 2]) for _ in range(34)]

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
        while check_nw(matrix, row, col, choose[rand]) | check_ne(row, col, choose[rand]) :
            rand = random.randint(0, len(choose)-1)
        matrix[row][col][0] = choose.pop(rand)
        row = row+1

    # South
    row = n_rows-1
    col = 1

    while col < n_cols-1 :
        rand = random.randint(0, len(choose)-1)
        while check_nw(matrix, row, col, choose[rand]) | check_sw(row, col, choose[rand]) :
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
#           Flask
# =============================

app = Flask(
    __name__,
    template_folder="templates",
    static_folder="static"
)

app.config["SECRET_KEY"] = ""

@app.errorhandler(404)
def not_found(e):
  return render_template("base.html")

@app.route("/")
def start():
    return render_template("hunt-the-wumpus.html", generate_grid(EASY, N_ROW, N_COL))

@app.route('/select-choose')
def select() :
    return render_template("select-choose.html")

@app.route('/settings')
def settings() :
    return render_template("settings.html")

@app.route('/title-screen')
def title() :
    return render_template("title-screen.html")

@app.route('/stats')
def stats():
    return render_template("stats.html")

@app.route('/menu')
def menu():
    return render_template('menu.html')

if __name__ == '__main__' :
    app.run(debug=True)
