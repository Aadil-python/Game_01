from flask import Flask, render_template, request, redirect, session
from flask_socketio import SocketIO, join_room, emit
import random

app = Flask(__name__)
app.secret_key = "secret"
socketio = SocketIO(app)

rooms = {}  # room_code: {players: [], numbers: {}}

# ---------------- ROUTES ----------------
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        session["username"] = request.form["username"]
        return redirect("/lobby")
    return render_template("login.html")

@app.route("/lobby", methods=["GET", "POST"])
def lobby():
    if request.method == "POST":
        room = request.form["room"]
        if room not in rooms:
            rooms[room] = {"players": [], "numbers": {}}
        return redirect(f"/game/{room}")
    return render_template("lobby.html", rooms=rooms)

@app.route("/game/<room>")
def game(room):
    return render_template("game.html", room=room, username=session["username"])

# ---------------- SOCKET ----------------
@socketio.on("join")
def on_join(data):
    room = data["room"]
    username = data["username"]

    join_room(room)

    if len(rooms[room]["players"]) < 2:
        rooms[room]["players"].append(username)
        emit("status", f"{username} joined", room=room)

    if len(rooms[room]["players"]) == 2:
        emit("start", room=room)

@socketio.on("choose_number")
def choose_number(data):
    room = data["room"]
    user = data["user"]
    number = int(data["number"])

    rooms[room]["numbers"][user] = number

    if len(rooms[room]["numbers"]) == 2:
        emit("both_ready", room=room)

@socketio.on("guess")
def guess(data):
    room = data["room"]
    guess = int(data["guess"])
    opponent = [p for p in rooms[room]["players"] if p != data["user"]][0]

    actual = rooms[room]["numbers"][opponent]

    if guess == actual:
        emit("win", data["user"], room=room)
    elif guess > actual:
        emit("result", {"msg": "LOWER", "num": guess}, room=room)
    else:
        emit("result", {"msg": "HIGHER", "num": guess}, room=room)

# ---------------- RUN ----------------
if __name__ == "__main__":
    socketio.run(app)
