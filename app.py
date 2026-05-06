#!/usr/bin/env python3
import os
from flask import Flask, render_template, redirect, request, session, flash
import random
from werkzeug.security import generate_password_hash, check_password_hash
import psycopg
from psycopg.rows import dict_row
from dotenv import load_dotenv

from db import get_connection
from p_game import *

# =============================
#           Flask
# =============================

app = Flask(
    __name__,
    template_folder="templates",
    static_folder="static"
)

app.config["SECRET_KEY"] = os.environ["THE_SECRET_KEY"]

@app.errorhandler(404)
def not_found(e):
  return render_template("base.html")

@app.route("/")
def home() :
    return redirect("/select-difficulty")

@app.route("/start")
def start() :
    print(session["difficulty"])
    print(session["blind"] )
    print(session["express"] )
    print("\n\n\n\n\n\n")
    if session.get("gamestate") == 0 :
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
    else :
        return redirect("/select-difficulty")

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
            session["difficulty"] = None
            return render_template("hunt-the-wumpus.html", grid=session["map"])
    else :
        return redirect("/select-difficulty")

@app.route('/select-difficulty', methods=["GET", "POST"])
def select() :
    user = None

    # Vérifier si l'utilisateur est connecté dans la session
    if 'username' in session:
        try:
            with get_connection() as conn:
                with conn.cursor(row_factory=dict_row) as cursor:
                    cursor.execute("SELECT * FROM user_table WHERE username = %s", (session['username'],))
                    user = cursor.fetchone()
        except Exception as e:
            print(f"Erreur lors de la récupération de l'utilisateur : {e}")

    if request.method == "POST":
        correct = False
        coord = request.form
        difficulty = coord.get("difficulty", type=int, default=1)
        express = coord.get("express", type=int, default=0)
        blind = coord.get("blind", type=int, default=0)

        correct = (difficulty in (EASY, NORMAL, HARD) and express in (0,1) and blind in (0,1))
        
        if correct : 
            session["difficulty"] = difficulty
            session["express"] = bool(express)
            session["blind"] = bool(blind)
            session["gamestate"] = 0
            # Ajouter une game au joueur
            return redirect("/start")
        else :
            return render_template("select-difficulty.html", 
                                   s_diff=session.get("difficulty", default=1),
                                   s_express=session.get("express", default=False), 
                                   s_blind=session.get("blind", default=False))
    else :
       return render_template("select-difficulty.html", 
                                   s_diff=session.get("difficulty", default=1),
                                   s_express=session.get("express", default=False), 
                                   s_blind=session.get("blind", default=False)) 
    # else:
    #     # Passer l'objet user au template
    #     return render_template("select-difficulty.html", user=user)

@app.route('/settings')
def settings() :
    return render_template("settings.html")

@app.route('/title-screen')
def title() :
    return render_template("title-screen.html")

@app.route('/stats')
def stats():
    users = []
    try:
        with get_connection() as conn:
            with conn.cursor(row_factory=dict_row) as cursor:
                cursor.execute("SELECT * FROM user_table ORDER BY score DESC LIMIT 12")
                users = cursor.fetchall()
    except Exception as e:
        flash(f"The error [ {e} ] has happened.", "danger")
    return render_template("stats.html", users = users)

@app.route('/login' , methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        try:
            with get_connection() as conn:
                with conn.cursor(row_factory=dict_row) as cursor:
                    cursor.execute("SELECT * FROM user_table WHERE username = %s", (username,))
                    user = cursor.fetchone()

                    print("Test : l'utilisateur est trouvé ! --> ", user)

                    if user and check_password_hash(user['pwd_hash'], password):
                        print("Connection en cours...")
                        session['user_id'] = user['id']
                        session['username'] = user['username']
                        flash("You are connected, welcome back!", "success")
                        return redirect("/play")

                    else:
                        flash("Your username or password is incorrect. Please check, and retry.", "danger")
                        return redirect("/login")

        except Exception as e:
            flash(f"An error has occured ; {e}", "danger")
    return render_template("login.html")

@app.route('/menu')
def menu():
    return render_template('menu.html')

@app.route('/register' , methods=["GET", "POST"])
def register():
    if request.method == "POST" :
        username = request.form['username']
        password = request.form['password']

        pswd_hash = generate_password_hash(password)

        icon_base64 = request.form.get('icon')

        try:
            with get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT 1 FROM user_table WHERE username = %s", (username,))
                    doesExist = cursor.fetchone()

                    if doesExist :
                        flash("This account name has aleardy been taken.", "danger")
                        return redirect("/login")

                    cursor.execute("INSERT INTO user_table (username, pwd_hash, icon) VALUES (%s, %s, %s)", (username, pswd_hash, icon_base64))
                    conn.commit()

                    flash("Your account has been created, you can now log in !", "success")
                    return redirect("/login")

        except Exception as e:
            flash(f"An error has occured : {e}", "danger")

    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    flash("Goodbye !", "success")
    return redirect("/login")

if __name__ == '__main__' :
    app.run(debug=True)
