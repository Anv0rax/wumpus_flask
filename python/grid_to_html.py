#!/usr/bin/env python3

from flask import Flask, render_template
import random
import numpy as np
#from markupsafe import Markup

app = Flask(
    __name__,
    template_folder="../templates",
    static_folder="../static"
)

N_ROW = 6
N_COL = 8

EASY = [0,0,0,0,1,2]
NORMAL = [0,0,0,1,2]
HARD = [0,1,2]

matrix = [[0] * N_COL for _ in range(N_ROW)]

def generate_grid(difficulty) :
    # North
    col = 0

    while col < N_COL :
        matrix[0][col] = random.choice(difficulty)
        col = col+1
    
    # West
    row = 0

    while row < N_ROW :
        matrix[row][0] = random.choice(difficulty)
        row = row+1

    # Center
    row = 1

    while row < N_ROW-1:
        col = 1
        while col < len(matrix[row])-1 :
            rand = random.choice(difficulty)
            while check_nw(row, col, rand) :
                rand = random.choice(difficulty)

            matrix[row][col] = rand
            col = col+1
        row = row+1

    # East
    row = 1
    col = N_COL-1

    while row < N_ROW-1 :
        rand = random.choice(difficulty)
        while check_nw(row, col, rand) or check_ne(row, col, rand) :
            rand = random.choice(difficulty)
        matrix[row][col] = rand
        row = row+1

    # South
    row = N_ROW-1
    col = 1

    while col < N_COL-1 :
        rand = random.choice(difficulty)
        while check_nw(row, col, rand) or check_ne(row, col, rand) :
            rand = random.choice(difficulty)
        matrix[row][col] = rand
        col = col+1

    # s-e corner
    rand = random.choice(difficulty)
    while (check_corner(rand)) :
        rand = random.choice(difficulty)
    matrix[row][col] = rand
    col = col+1

    return matrix

# =============================
#           Check
# =============================

def check_nw(row, col, type) :
    retry = False
    match type :
        case 1 :
            if matrix[row-1][col] == 2 :
                if matrix[row][col-1] == 2 :
                    if (matrix[row-1][col-1] == 1) :
                        retry = True
        case 2 :
            if matrix[row-1][col] == 1 :
                if matrix[row][col-1] == 1 :
                    if (matrix[row-1][col-1] == 2) :
                        retry = True
    return retry

def check_ne(row, col, type) :
    retry = False
    match type :
        case 1 :
            if matrix[row-1][col] == 2 :
                if matrix[row][0] == 2 :
                    if (matrix[row-1][0] == 1) :
                        retry = True
        case 2 :
            if matrix[row-1][col] == 1 :
                if matrix[row][0] == 1 :
                    if (matrix[row-1][0] == 2) :
                        retry = True
    return retry

def check_sw(row, col, type) :
    retry = False
    match type :
        case 1 :
            if matrix[0][col] == 2 :
                if matrix[row][col-1] == 2 :
                    if (matrix[0][col-1] == 1) :
                        retry = True
        case 2 :
            if matrix[0][col] == 1 :
                if matrix[row][col-1] == 1 :
                    if (matrix[0][col-1] == 2) :
                        retry = True
    return retry

def check_corner(type) :
    row = N_ROW-1
    col = N_COL-1

    retry = False
    match type :
        case 1 :
            if matrix[row-1][col] == 2 : #↑
                if matrix[row][col-1] == 2 : #←
                    if matrix[row][0] == 2 : #→
                        if matrix[row-1][col-1] == 1 : #←↑
                            retry = True
            if matrix[0][col] == 2 : #↓
                if matrix[row][col-1] == 2 : #←
                    if matrix[row][0] == 2 : #→
                        if matrix[0][0] == 1 : #↓→
                            retry = True
        case 2 :
            if matrix[row-1][col] == 1 : #↑
                if matrix[row][col-1] == 1 : #←
                    if matrix[row][0] == 1 : #→
                        if matrix[row-1][col-1] == 2 : #←↑
                            retry = True
            if matrix[0][col] == 1 : #↓
                if matrix[row][col-1] == 1 : #←
                    if matrix[row][0] == 1 : #→
                        if matrix[0][0] == 2 : #↓→
                            retry = True
    return retry

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