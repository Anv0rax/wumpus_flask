#!/usr/bin/env python3

from flask import Flask, render_template, redirect, request, session
import random
from werkzeug.security import generate_password_hash, check_password_hash
import psycopg


from p_game import *
from p_input_validity import *



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
def not_found(e) :
  return render_template("base.html")

@app.route("/")
def home() :
    return redirect("/start")

@app.route("/start")
def start() :
    difficulty = EASY
    matrix = generate_grid(difficulty)
    while not flood_fill_map(matrix) :
        matrix = generate_grid(difficulty)
        print("\n\n\n\n\nMap regen\n\n\n\n")

    hole_1 = random_init(matrix, val=HOLE)
    generate_around(matrix, hole_1, type=N_HOLE)
    hole_2 = random_init(matrix, val=HOLE)
    generate_around(matrix, hole_2, type=N_HOLE)

    wumpus = random_init(matrix, val=WUMPUS)
    generate_around(matrix, wumpus, type=N_WUMP)

    bat = random_init(matrix, val=BAT)
    matrix[bat[0]][bat[1]][T_ELEMS] += BAT
    if difficulty > EASY :
        bat = random_init(matrix, val=BAT)
        matrix[bat[0]][bat[1]][T_ELEMS] += BAT

    # now generate elements
    session["player"] = init_player(matrix)
    session["map"] = matrix
    return redirect("/play")

@app.route("/play")
def play() :
    if session.get("map") and session.get("player") :
        coord = request.args
        x = coord.get('x', type=int, default=0)
        y = coord.get('y', type=int, default=0)
        if verify_move((y,x)) :
            player = session.get("player")
            moved = move_item(session["map"], player[0], player[1], y, x)
            if moved[0] :
                player = (moved[1], moved[2])
                session["player"] = player
                if session.get('express', default=False) \
                 and not session["map"][player[0]][player[1]][T_BOX] == CAVERN :
                    session["player"] = follow_corridor(session["map"], player[0], player[1], y, x)
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
