#!/usr/bin/env python3
import os
import re
from flask import Flask, render_template, redirect, request, session, flash
import random
from werkzeug.security import generate_password_hash, check_password_hash
import psycopg
from psycopg.rows import dict_row
from dotenv import load_dotenv

from db import get_connection
from p_game import *
from private import THE_SECRET_KEY

# =============================
#           Flask
# =============================

app = Flask(
    __name__,
    template_folder="templates",
    static_folder="static"
)

app.config["SECRET_KEY"] = THE_SECRET_KEY

def finish_game(result_code):
    if 'username' not in session :
        return

    column_map = {
        -1: "numberofvictories",
        -2: "defeats",
        -3: "fell_slime_pit",
        -4: "missed",
        3: "bat_touched"
    }

    column_to_update = column_map.get(result_code)

    if not column_to_update:
        return

    points = 0
    if result_code == -1:
        points = (session.get('difficulty', 0) + 1) * 10

    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                query = f"""UPDATE user_table SET {column_to_update} = {column_to_update} + 1, score = score + %s WHERE username = %s"""
                cursor.execute(query, (points, session['username']))
                conn.commit()
    except Exception as e:
        print(f"Error, couldn't register the new value of the score : {e}")

@app.context_processor
def inject_user():
    user = None
    if 'username' in session :
        try:
            with get_connection() as conn:
                with conn.cursor(row_factory=dict_row) as cursor:
                    cursor.execute("SELECT * FROM user_table WHERE username = %s", (session['username'],))
                    user = cursor.fetchone()
        except Exception as e:
            print(f"Error, user surely not found : {e}")
    # La variable 'user' sera maintenant accessible dans TOUS les fichiers .html.
    # je vais donc pouvoir avoir accès aux infos de l'user quand il est connecté pour pouvoir afficher son image
    return dict(user=user)

@app.errorhandler(404)
def not_found(e):
    return render_template("base.html"), 404

@app.route("/")
def home() :
    return redirect("/menu")

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

@app.route("/menu")
def menu():
    return render_template("main_page.html")


@app.route("/play")
def play() :
    if 'username' not in session:
        flash("Please be connected to play !", "danger")
        return redirect("/login")

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
                                finish_game(3)
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
                                finish_game(i)
                                match i :
                                    case -1 : # Win
                                        print("\n\n\nWin")
                                        flash("YOU WIN ! You have killed the wumpus, congratulations !", "success")

                                    case -2 : # Wumpus
                                        print("\n\n\nLoose by wumpus")
                                        flash("YOU LOSE ! The wumpus got you.", "danger")

                                    case -3 : # Hole
                                        print("\n\n\nLoose by hole")
                                        flash("YOU LOSE ! You fell into the slime pit...", "danger")

                                    case -4 : # Missed
                                        print("\n\n\nLoose by missing")
                                        flash("YOU LOSE ! You shoot your only arrow !", "danger")

                                session["gamestate"] = -9

                    session["player"] = player
                else :
                    reveal_map(matrix)
                    player_pos = matrix[player[0]][player[1]][T_PLAYER]

                    session["gamestate"] = shoot_arrow(matrix, player, y, x)
                    matrix[player[0]][player[1]][T_PLAYER] = player_pos

                    if session["gamestate"] == -1:
                        print("\n\n\nWIN\n")
                        flash("YOU WIN ! You have killed the wumpus, congratulations !", "success")
                    else:
                        print("\n\n\nYOU LOSE, MISSED THE WUMPUS !\n")
                        flash("YOU LOSE ! You shoot your only arrow !", "danger")

                    finish_game(session["gamestate"])

                    session["gamestate"] = -9

                session["map"] = matrix

            return render_template("hunt-the-wumpus.html", grid=session["map"])
        elif session.get("gamestate") < 0 :
            session["difficulty"] = None
            return render_template("hunt-the-wumpus.html", grid=session["map"])
    else :
        return redirect("/select-difficulty")

@app.route('/select-difficulty', methods=["GET", "POST"])
def select() :
    if 'username' not in session:
        flash("Please be connected to play !", "danger")
        return redirect("/login")

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


@app.route('/settings', methods=["GET", "POST"])
def settings():
    if 'username' not in session :
        flash("Please, log into the site or create a account to see your account.", "danger")
        return redirect("/login")

    if request.method == "POST":
        icon_data = request.form.get("icon")
        if icon_data:
            try:
                with get_connection() as conn:
                    with conn.cursor() as cursor:
                        cursor.execute(
                            "UPDATE user_table SET icon = %s WHERE username = %s",
                            (icon_data, session['username'])
                        )
                        conn.commit()
                flash("Icon updated !", "success")
            except Exception as e:
                flash(f"SQL error : {e}", "danger")
            return redirect("/settings")

    user_ranks = None
    try:
        with get_connection() as conn:
            with conn.cursor(row_factory=dict_row) as cursor:
                query = "SELECT username, RANK() OVER (ORDER BY score DESC) as rank_score, RANK() OVER (ORDER BY numberofvictories DESC) as rank_wins, RANK() OVER (ORDER BY defeats ASC) as rank_survivor, RANK() OVER (ORDER BY bat_touched DESC) as rank_bats, RANK() OVER (ORDER BY missed ASC) as rank_missed, RANK() OVER (ORDER BY fell_slime_pit ASC) as rank_slime FROM user_table"
                cursor.execute(query)
                all_players_ranks = cursor.fetchall()

                user_ranks = next((r for r in all_players_ranks if r['username'] == session['username']), None)

    except Exception as e:
        print(f"Error fetching ranks: {e}")

    return render_template("settings.html",ranks=user_ranks)

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

@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm', '')
        icon_base64 = request.form.get('icon', '')

        if not re.match(r"^[a-zA-Z0-9_]{3,10}$", username):
            flash("Username must be between 3 and 10 characters (letters, numbers, underscores).", "danger")
            return redirect("/register")

        if not (re.match(r"^.{3,10}$", password) and
                re.search(r"[A-Z]", password) and
                re.search(r"[a-z]", password) and
                re.search(r"[0-9]", password)):
            flash("Password must be 3-10 characters long and contain at least one uppercase, one lowercase, and one number.", "danger")
            return redirect("/register")

        if password != confirm_password:
            flash("Passwords are not matching.", "danger")
            return redirect("/register")

        try:
            pswd_hash = generate_password_hash(password)
            with get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT 1 FROM user_table WHERE username = %s", (username,))
                    if cursor.fetchone():
                        flash("This username is already taken.", "danger")
                        return redirect("/register")

                    cursor.execute(
                        "INSERT INTO user_table (username, pwd_hash, icon) VALUES (%s, %s, %s)",
                        (username, pswd_hash, icon_base64)
                    )
                    conn.commit()

            flash("Your account has been created, you can now log in!", "success")
            return redirect("/login")

        except Exception as e:
            flash(f"An error occurred: {e}", "danger")
            return redirect("/register")

    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    flash("Goodbye !", "success")
    return redirect("/login")

if __name__ == '__main__' :
    app.run(debug=True)
