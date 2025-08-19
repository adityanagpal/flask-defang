import os

from flask import Flask, jsonify, request, render_template_string, render_template
import random

app = Flask(__name__)

# A simple in-memory structure to store tasks
tasks = []

# @app.route('/', methods=['GET'])
# def home():
#     # Display existing tasks and a form to add a new task
#     html = '''
# <!DOCTYPE html>
# <html>
# <head>
#     <title>Todo List</title>
# </head>
# <body>
#     <h1>Todo List</h1>
#     <form action="/add" method="POST">
#         <input type="text" name="task" placeholder="Enter a new task">
#         <input type="submit" value="Add Task">
#     </form>
#     <ul>
#         {% for task in tasks %}
#         <li>{{ task }} <a href="/delete/{{ loop.index0 }}">Delete</a></li>
#         {% endfor %}
#     </ul>
# </body>
# </html>
# '''
#     return render_template_string(html, tasks=tasks)


def is_valid_move(board, row, col, num):
    if num in board[row]:
        return False
    if num in [board[i][col] for i in range(9)]:
        return False
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(start_row, start_row + 3):
        for j in range(start_col, start_col + 3):
            if board[i][j] == num:
                return False
    return True

def is_solved(board):
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                return False
            if not is_valid_move(board, i, j, board[i][j]):
                return False
    return True

def generate_board():
    board = [[0] * 9 for _ in range(9)]
    for _ in range(120):
        row, col, num = random.randint(0, 8), random.randint(0, 8), random.randint(1, 9)
        if board[row][col] == 0 and is_valid_move(board, row, col, num):
            board[row][col] = num
    return board

# -----------------
# Game State
# -----------------
game_state = {"board": generate_board()}

# -----------------
# API Endpoints
# -----------------
@app.route("/")
def index():
    print(os.getcwd())
    return render_template("index.html")

@app.route("/new", methods=["GET"])
def new_game():
    game_state["board"] = generate_board()
    return jsonify({"board": game_state["board"]})

@app.route("/board", methods=["GET"])
def get_board():
    return jsonify({"board": game_state["board"]})

@app.route("/move", methods=["POST"])
def make_move():
    data = request.json
    row = data.get("row")
    col = data.get("col")
    num = data.get("num")

    if not (0 <= row < 9 and 0 <= col < 9 and 1 <= num <= 9):
        return jsonify({"error": "Invalid input"}), 400
    if game_state["board"][row][col] != 0:
        return jsonify({"error": "Cell already filled"}), 400

    if is_valid_move(game_state["board"], row, col, num):
        game_state["board"][row][col] = num
        return jsonify({"success": True, "board": game_state["board"]})
    else:
        return jsonify({"error": "Invalid move"}), 400

@app.route("/check", methods=["GET"])
def check_solution():
    return jsonify({"solved": is_solved(game_state["board"])})
@app.route('/add', methods=['POST'])
def add_task():
    # Add a new task from the form data
    task = request.form.get('task')
    if task:
        tasks.append(task)
    return home()

@app.route('/delete/<int:index>', methods=['GET'])
def delete_task(index):
    # Delete a task based on its index
    if index < len(tasks):
        tasks.pop(index)
    return home()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
