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
def not_found(e):
  return render_template("base.html")

@app.route("/")
def home():
    return redirect("/start")

@app.route("/start")
def start():
    matrix = generate_grid(HARD, N_ROW, N_COL)
    for i in range(1000) :
        try :
            maptest = generate_grid(HARD, N_ROW, N_COL)
            flood_fill_map(maptest, N_ROW, N_COL, HARD)
        except : 
            matrix = maptest
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
