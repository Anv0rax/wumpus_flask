#!/usr/bin/env python3

from flask import Flask, render_template, redirect, request, session
import random
from werkzeug.security import generate_password_hash, check_password_hash
import psycopg

from p_game import *

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
    session["difficulty"] = EASY
    session["blind"] = False
    session["express"] = False
    difficulty = session.get("difficulty")
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

    n = 2 if difficulty > EASY else 1
    for i in range(n) :
        bat = random_init(matrix, val=BAT)
        matrix[bat[0]][bat[1]][T_ELEMS] += BAT

    hide_map(matrix)
    session["player"] = init_player(matrix)
    session["map"] = matrix
    session["gamestate"] = 1
    return redirect("/play")

@app.route("/play")
def play() :
    if session.get("map") and session.get("player") :
        if session.get("gamestate", default=0) > 0 :
            coord = request.args
            shoot = coord.get("shoot", type=bool, default=False)
            x = coord.get("x", type=int, default=0)
            y = coord.get("y", type=int, default=0)

            if verify_move((y,x)) :
                player = session.get("player")
                matrix = session.get("map")
                if not shoot :
                    moved = move_item(matrix, player[0], player[1], y, x, 
                                    blind=session.get("blind", default=False))

                    if moved[0] :
                        player = (moved[1], moved[2])

                        if session.get("express", default=False) \
                        and matrix[player[0]][player[1]][T_BOX] not in (CAVERN, N_HOLE, HOLE) :
                            player = follow_corridor(matrix, player[0], player[1], y, x, blind=session.get("blind", default=False))

                        session["gamestate"] = check_player(matrix, player)
                        
                        match session.get("gamestate") :
                            # case 2 : # add to bd
                            case 3 : # walked on a triggered bat
                                # remove bat and player
                                matrix[player[0]][player[1]][T_ELEMS] -= TRIG_BAT
                                matrix[player[0]][player[1]][T_PLAYER] = IS_NOT_HERE
                                matrix[player[0]][player[1]][T_VISION] = not session.get("blind", default=False)
                                # add new bat
                                bat = random_init(matrix, val=BAT)
                                matrix[bat[0]][bat[1]][T_ELEMS] += BAT
                                # move player
                                player = init_player(matrix)
                            case i if i < 0 :
                                reveal_map(matrix)
                                # finish_in_db(i)
                                match i :
                                    case -1 : # Win
                                        print("\n\n\nWin")
                                        # write in BD

                                    case -2 : # Wumpus
                                        print("\n\n\nLoose by wumpus")
                                        # write in BD

                                    case -3 : # Hole
                                        print("\n\n\nLoose by hole")
                                        # write in BD

                                    case -4 : # Missed
                                        print("\n\n\nLoose by missing")
                                        # write in BD

                                session["gamestate"] = -9

                    session["player"] = player
                else :
                    reveal_map(matrix)
                    player_pos = matrix[player[0]][player[1]][T_PLAYER]
                    session["gamestate"] = shoot_arrow(matrix, player, y, x)
                    matrix[player[0]][player[1]][T_PLAYER] = player_pos 

                    print("\n\n\nWIN\n")
                    # finish_in_db(session.get("gamestate"))
                    # write in BD
                session["map"] = matrix

            return render_template("hunt-the-wumpus.html", grid=session["map"])
        elif session.get("gamestate") < 0 :
            return render_template("hunt-the-wumpus.html", grid=session["map"])
    else :
        return redirect("/select-difficulty")

@app.route("/select-difficulty", methods=["GET", "POST"])
def select() :
    if request.method == "POST" :
        return redirect("/start")
    else :
        return render_template("select-difficulty.html")

@app.route("/settings")
def settings() :
    return render_template("settings.html")

@app.route("/title-screen")
def title() :
    return render_template("title-screen.html")

@app.route("/stats")
def stats():
    return render_template("stats.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/menu")
def menu():
    return render_template("menu.html")

if __name__ == "__main__" :
    app.run(debug=True)
