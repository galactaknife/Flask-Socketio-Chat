from flask import Flask, redirect, url_for, render_template, request, session, Markup
from flask_socketio import SocketIO, send, emit
import random
import chatbot as cb

app = Flask(__name__)
app.secret_key = "doodoocaca"
socketio = SocketIO(app)

users = {}
colors = {}

@app.route('/')
def index():
    if "user" in session:
        user = session["user"]
        colors[user] = random.choice(["#3399ff", "#953d96", "#e0383e", "#62ba46", "#f7821b", "lightSeaGreen", "steelBlue", "darkGoldenrod", "orangeRed", "#a83299", "#246b62", "teal", "royalBlue", "saddleBrown", "crimson", "green", "#607d46", "indianRed", "mediumVioletRed", "darkOrange", "olive", "gray", "mediumPurple", "#71268c"])
        return render_template("index.html", username=Markup("<span class='name' style='background-color: " + colors[user] + "'>" + user + "</span>"))
    else:
        return redirect(url_for("login"))

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        user = request.form["nm"]
        if user in users.values():
            return render_template("login.html", flash="Username taken")
        session["user"] = user
        return redirect(url_for("index"))
    else:
        try:
            if request.sid in users:
                return redirect(url_for("index"))
        except:
            return render_template("login.html")

@app.route("/logout", methods=["POST", "GET"])
def logout():
    leave()
    return redirect(url_for("login"))

@socketio.on("login")
def loginMessage(user):
    emit("message", user + "logged in", broadcast=True, namespace='/')

@socketio.on("connect")
def connect():
    for i in users.values():
        if session["user"] == i:
            del users[list(users.keys())[list(users.values()).index(session["user"])]]
    users[request.sid] = session["user"]
    emit("users", [list(users.values()), colors], broadcast=True, namespace='/')

@socketio.on("disconnect")
def leave():
    session.pop("user", None)
    try:
        users.pop(request.sid)
    except:
        pass
    emit("users", [list(users.values()), colors], broadcast=True, namespace='/')

@socketio.on("message")
def loginMessage(message):
    if request.sid in users:
        emit("message", [colors[session["user"]], session["user"], message], broadcast=True, namespace='/')
        if "//" in message:
            emit("message", ["chatbot", cb.analyze(message)], broadcast=True, namespace='/')

    else:
        return redirect(url_for("login"))

socketio.run(host='0.0.0.0', port=PORT, debug=False)
