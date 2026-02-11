from flask import Flask, render_template
import random
#from markupsafe import Markup

app = Flask(
    __name__,
    template_folder="../templates",
    static_folder="../static"
)

EASY = [0,0,0,1,2]
NORMAL = [0,0,1,2]
HARD = [0,1,2]

def generate_grid(difficulty):
    matrix = [
        [ 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 ],
        [ 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 ],
        [ 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 ],
        [ 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 ],
        [ 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 ],
        [ 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 ]
    ]
    
    row = 0
    col = 0

    while col < len(matrix[0]):
        matrix[row][col] = random.choice(difficulty)
        col = col+1
    
    while row < len(matrix):
        matrix[row][0] = random.choice(difficulty)
        row = row+1

    row = 1

    while row < len(matrix)-1:
        col = 1
        while col < len(matrix[row])-1 :
            rand = random.choice(difficulty)
            while grid_retry_next(matrix, row, col, rand):
                rand = random.choice(difficulty)
            matrix[row][col] = rand
            col = col+1
        row = row+1
    return matrix

def grid_retry_next(matrix, row, col, type) :
    retry = False
    match type:
        case 1:
            if matrix[row+1][col] == 2 :
                if matrix[row][col+1] == 2 :
                    if (matrix[row+1][col+1] == 1) :
                        retry = True
        case 2:
            if matrix[row+1][col] == 1 :
                if matrix[row][col+1] == 1 :
                    if (matrix[row+1][col+1] == 2) :
                        retry = True
    # matrix[(row+1)%N_ROW][(col+1)%N_COL]
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