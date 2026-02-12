#!/usr/bin/env python3

from flask import Flask, render_template
import random
#from markupsafe import Markup

N_ROW = 6
N_COL = 8

EASY = 0
NORMAL = 1
HARD = 2

matrix = [[0] * N_COL for _ in range(N_ROW)]

def generate_grid(diff) :
    match diff :
        case 0 :
            difficulty = [0]*40 + [random.choice([1, 2]) for _ in range(14)]
        case 1 :
            difficulty = [0]*30 + [random.choice([1, 2]) for _ in range(24)]
        case 2 :
            difficulty = [0]*20 + [random.choice([1, 2]) for _ in range(34)]

    # North
    col = 0

    while col < N_COL :
        matrix[0][col] = difficulty.pop(random.randint(0, len(difficulty)-1))
        col = col+1
    
    # West
    row = 0

    while row < N_ROW :
        matrix[row][0] = difficulty.pop(random.randint(0, len(difficulty)-1))
        row = row+1

    # Center
    row = 1

    while row < N_ROW-1:
        col = 1
        while col < len(matrix[row])-1 :
            rand = random.randint(0, len(difficulty)-1)
            while check_nw(row, col, difficulty[rand]) :
                rand = random.randint(0, len(difficulty)-1)

            matrix[row][col] = difficulty.pop(rand)
            col = col+1
        row = row+1

    # East
    row = 1
    col = N_COL-1

    while row < N_ROW-1 :
        rand = random.randint(0, len(difficulty)-1)
        while check_nw(row, col, difficulty[rand]) | check_ne(row, col, difficulty[rand]) :
            rand = random.randint(0, len(difficulty)-1)
        matrix[row][col] = difficulty.pop(rand)
        row = row+1

    # South
    row = N_ROW-1
    col = 1

    while col < N_COL-1 :
        rand = random.randint(0, len(difficulty)-1)
        while check_nw(row, col, difficulty[rand]) | check_sw(row, col, difficulty[rand]) :
            rand = random.randint(0, len(difficulty)-1)
        matrix[row][col] = difficulty.pop(rand)
        col = col+1

    # Corner
    rand = random.randint(0, len(difficulty)-1)
    stop_while = 0
    while (check_corner(difficulty[rand])) and stop_while < 5 :
        rand = random.randint(0, len(difficulty)-1)
        stop_while = stop_while+1
    if stop_while == 5 :
        matrix[row][col] = 0
    else :
        matrix[row][col] = difficulty.pop(rand)
    col = col+1

    return matrix

# =============================
#           Check

def check_nw(row, col, type) :
    retry = False
    if type == 2 :
        if matrix[row-1][col] == 1 :
            if matrix[row][col-1] == 1 :
                if (matrix[row-1][col-1] == 2) :
                    retry = True
    return retry

def check_ne(row, col, type) :
    retry = False
    if type == 1 :
        if matrix[row-1][col] == 2 :
            if matrix[row][0] == 2 :
                if (matrix[row-1][0] == 1) :
                    retry = True
    return retry

def check_sw(row, col, type) :
    retry = False
    if type == 1 :
        if matrix[0][col] == 2 :
            if matrix[row][col-1] == 2 :
                if (matrix[0][col-1] == 1) :
                    retry = True
    return retry

def check_se(row, col, type) :
    retry = False
    if type == 2 :
        if matrix[0][col] == 1 :
            if matrix[row][0] == 1 :
                if (matrix[0][0] == 2) :
                    retry = True
    return retry

def check_corner(type) :
    row = N_ROW-1
    col = N_COL-1

    retry = False
    match type :
        case 1 :
            retry = check_ne(row, col, type) | check_sw(row, col, type)
        case 2 :
            retry = check_nw(row, col, type) | check_se(row, col, type)
    return retry




# =============================
#           Flask
# =============================

app = Flask(
    __name__,
    template_folder="templates",
    static_folder="static"
)

@app.route("/")
def start():
    row = 0
    matrix = generate_grid(HARD)
    while row < len(matrix):
        colmn = 0
        while colmn < len(matrix[row]) :
            match matrix[row][colmn] :
                case 0:
                    css_class = "normal"
                case 1:
                    css_class = "corridor_1"
                case 2:
                    css_class = "corridor_2"
            matrix[row][colmn] = css_class
            colmn = colmn+1
        row = row+1
    #return render_template("hunt-the-wumpus.html", grid=matrix, params=Markup('<div id="player" class="top-1"></div>'))
    return render_template(
        "hunt-the-wumpus.html",
        grid=matrix,
        params='<div id="player" class="top-1"></div><div class="bat"></div>')

if __name__ == '__main__' :
    app.run(debug=True)