from flask import Flask, redirect, url_for, render_template, request, session, Markup
from flask_socketio import SocketIO, emit, join_room, leave_room, disconnect
import random, json
from flask_cors import CORS, cross_origin
import chatbot as cb

# Initialize app
app = Flask(__name__)
cors = CORS(app)
app.secret_key = "tan the man"
socketio = SocketIO(app, cors_allowed_origins="*")

# Holds all rooms and room data
rooms = {
    "Room 1" : {
        "users" : {},
        "colors" : {},
        "banned" : []
    },
    "Room 2" : {
        "users" : {},
        "colors" : {},
        "banned" : []
    },
    "Room 3" : {
        "users" : {},
        "colors" : {},
        "banned" : []
    }
}

# Holds name of added rooms
addedRooms = []
# Holds name of user and what room they're in
userRoom = {}

@app.route('/', methods=["POST", "GET"])
def index():
    try:
        # If user is logged in, send to chat page
        if "user" in session:
            # Initialize chat page
            user = session["user"]
            if user == "Admin":
                rooms[userRoom[session["user"]]]["colors"][user] = "darkred"
            else:
                rooms[userRoom[session["user"]]]["colors"][user] = random.choice(["#3399ff", "#953d96", "#e0383e", "#62ba46", "#f7821b", "lightSeaGreen", "steelBlue", "darkGoldenrod", "orangeRed", "#a83299", "#246b62", "teal", "royalBlue", "saddleBrown", "crimson", "green", "#607d46", "indianRed", "mediumVioletRed", "darkOrange", "olive", "gray", "mediumPurple", "#71268c"])
            return render_template("index.html", username=Markup("<span class='name' style='background-color: " + rooms[userRoom[session["user"]]]["colors"][user] + "'>" + user + "</span>"), room=userRoom[session["user"]])
        # If user isn't logged in, redirect to login
        else:
            return redirect(url_for("login"))
    except:
        return redirect(url_for("login"))

@app.route("/login", methods=["POST", "GET"])
def login():
    # If user logs in, get username and redirect to chat page
    if request.method == "POST":
        user = request.form["nm"].replace('@', '').replace(' ', '_')
        # If username is Admin, request a password
        if user == "Admin":
            try:
                if request.form["pass"]:
                    # If valid password, redirect to chat
                    if not request.form["pass"] == "admin password":
                        return render_template("login.html", rooms=rooms.keys(), passReq=user)
                else:
                    return render_template("login.html", rooms=rooms.keys())
            except:
                return render_template("login.html", rooms=rooms.keys(), passReq=user)
        # If a user already exists with selected  username, redirect to login
        if user in userRoom.keys() or user in rooms.keys() or user == "chatbot":
            return render_template("login.html", rooms=rooms.keys(), flash="Username taken")
        userRoom[user] = request.form["rooms"]
        session["user"] = user
        return redirect(url_for("index"))
    # Redirect to login if get method
    else:
        return render_template("login.html", rooms=rooms.keys())

@app.route("/logout", methods=["POST", "GET"])
def logout():
    # If user logs out, redirect to login page
    return redirect(url_for("login"))

@socketio.on("login")
def loginMessage(user):
    # On login, send login message to current chatroom
    try:
        emit("message", user + "logged in", broadcast=True, namespace='/', room=userRoom[session["user"]])
    except:
        pass

@socketio.on("connect")
def connect():
    # When user joins, reset all past data if neccessary
    try:
        if session["user"] in rooms[userRoom[session["user"]]]["users"].values():
            del rooms[userRoom[session["user"]]]["users"][list(rooms[userRoom[session["user"]]]["users"].keys())[list(rooms[userRoom[session["user"]]]["users"].values()).index(session["user"])]]
    except:
        pass
    # Joins room and initializes user
    try:
        join_room(userRoom[session["user"]])
        join_room(session["user"])
        rooms[userRoom[session["user"]]]["users"][request.sid] = session["user"]
        emit("users", [list(rooms[userRoom[session["user"]]]["users"].values()), json.dumps(rooms[userRoom[session["user"]]]["colors"])], broadcast=True, namespace='/', room=userRoom[session["user"]])
    except:
        emit("alert", "Session expired.  Reload page to send messages.", namespace='/')

@socketio.on("disconnect")
def leave():
    # On disconnect, delete user from room and remove session
    try:
        emit("message", [rooms[userRoom[session["user"]]]["colors"][session["user"]], session["user"], "left the chat"], broadcast=True, namespace='/', room=userRoom[session["user"]])
        room = userRoom[session["user"]]
        leave_room(userRoom[session["user"]])
        leave_room(session["user"])
        try:
            del rooms[userRoom[session["user"]]]["colors"][session["user"]]
        except:
            pass
        rooms[userRoom[session["user"]]]["users"] = {key:val for key, val in rooms[userRoom[session["user"]]]["users"].items() if val != session["user"]}
        emit("users", [list(rooms[userRoom[session["user"]]]["users"].values()), json.dumps(rooms[userRoom[session["user"]]]["colors"])], broadcast=True, namespace='/', room=room)
        del userRoom[session["user"]]
        session.pop("user", None)
    except:
        pass

@socketio.on("message")
def message(message):
    try:
        # If user is banned, don't allow message to be sent
        if session["user"] in rooms[userRoom[session["user"]]]["users"].values():
            if session["user"] in rooms[userRoom[session["user"]]]["banned"]:
                emit("message", ["chatbot", "You are banned from " + userRoom[session["user"]]], namespace='/', room=session["user"])

            # Sends private message if applicable
            elif '@' in message:
                sendee = list(message.split(' '))
                emit("message", [rooms[userRoom[session["user"]]]["colors"][session["user"]], session["user"], message, "private"], broadcast=True, namespace='/', room=session["user"])
                # Will prevent duplicate messages being sent to the same person
                sentTo = []
                for i in sendee:
                    i = i.replace(',', '')
                    try:
                        # If '@' detected, send message to corresponding person if real user
                        if i[0] == '@':
                            if i not in sentTo and not i[1:] == session["user"]:
                                if i[1:] in userRoom.keys() and not i[1:] in rooms[userRoom[session["user"]]]["users"].values():
                                    sentTo.append(i)
                                    emit("message", [rooms[userRoom[session["user"]]]["colors"][session["user"]], session["user"], message, "private", userRoom[session["user"]]], namespace='/', room=i[1:])
                                elif i[1:] in userRoom.keys():
                                    sentTo.append(i)
                                    emit("message", [rooms[userRoom[session["user"]]]["colors"][session["user"]], session["user"], message, "private"], broadcast=True, namespace='/', room=i[1:])
                                else:
                                    emit("message", ["darkslategray", "chatbot", "User " + i[1:] + " doesn't exist"], broadcast=True, namespace='/', room=session["user"])
                    except:
                        pass

            # Adds room if prompted by Admin
            elif session["user"] == "Admin" and "// new room=" in message.lower():
                emit("message", [rooms[userRoom[session["user"]]]["colors"][session["user"]], session["user"], message], broadcast=True, namespace='/', room=userRoom[session["user"]])
                newRoom = list(message.split('='))[1]
                # If room doesn't exist, create new room
                if not newRoom in addedRooms:
                    addedRooms.append(newRoom)
                    rooms[newRoom] = {"users" : {}, "colors" : {}, "banned" : []}
                    emit("message", ["chatbot", "Created room " + newRoom], broadcast=True, namespace='/', room=userRoom[session["user"]])
                else:
                    emit("message", ["chatbot", "Room " + newRoom + " already exists"], broadcast=True, namespace='/', room=userRoom[session["user"]])

            # Deletes room if prompted by Admin
            elif session["user"] == "Admin" and "// del room=" in message.lower():
                emit("message", [rooms[userRoom[session["user"]]]["colors"][session["user"]], session["user"], message], broadcast=True, namespace='/', room=userRoom[session["user"]])
                delRoom = list(message.split('='))[1]
                # If room is a real room, remove room
                if delRoom in addedRooms:
                    addedRooms.remove(delRoom)
                    del rooms[delRoom]
                    emit("message", ["chatbot", "Deleted room " + delRoom], broadcast=True, namespace='/', room=userRoom[session["user"]])
                    emit("alert", "This chat room has been deleted by " + session["user"], broadcast=True, namespace='/', room=delRoom)
                else:
                    emit("message", ["chatbot", "Can't delete room " + delRoom], broadcast=True, namespace='/', room=userRoom[session["user"]])

            # Show all bans if prompted by Admin
            elif session["user"] == "Admin" and "// bans" in message:
                bannedStr = 'Banned users: '
                for i in rooms[userRoom[session["user"]]]["banned"]:
                    bannedStr += i + ' '
                if bannedStr == '':
                    bannedStr = "Currently, there are no banned users"
                emit("message", [rooms[userRoom[session["user"]]]["colors"][session["user"]], session["user"], message], broadcast=True, namespace='/', room=userRoom[session["user"]])
                emit("message", ["chatbot", bannedStr], broadcast=True, namespace='/', room=userRoom[session["user"]])

            # Bans user if name is Admin
            elif session["user"] == "Admin" and "// ban" in message and not "Admin" in message:
                userToBan = message.replace('// ban', '').strip()
                rooms[userRoom[session["user"]]]["banned"].append(userToBan)
                emit("message", [rooms[userRoom[session["user"]]]["colors"][session["user"]], session["user"], message], broadcast=True, namespace='/', room=userRoom[session["user"]])
                emit("message", ["chatbot", userToBan + " has been banned from " + userRoom[session["user"]] + " by " + session["user"]], broadcast=True, namespace='/', room=userRoom[session["user"]])

            # Unbans user if name is Admin
            elif session["user"] == "Admin" and "// unban" in message:
                userToUnban = message.replace('// unban', '').strip()
                # If user is banned, unban them
                try:
                    rooms[userRoom[session["user"]]]["banned"].remove(userToUnban)
                    emit("message", [rooms[userRoom[session["user"]]]["colors"][session["user"]], session["user"], message], broadcast=True, namespace='/', room=userRoom[session["user"]])
                    emit("message", ["chatbot", userToUnban + " has been unbanned from " + userRoom[session["user"]] + " by " + session["user"]], broadcast=True, namespace='/', room=userRoom[session["user"]])
                except:
                    emit("message", [rooms[userRoom[session["user"]]]["colors"][session["user"]], session["user"], message], broadcast=True, namespace='/', room=userRoom[session["user"]])
                    emit("message", ["chatbot", Markup("User <em>" + userToUnban + "</em> isn't banned")], broadcast=True, namespace='/', room=userRoom[session["user"]])

            # Clears all bans if name is Admin
            elif session["user"] == "Admin" and "// clearban" in message:
                rooms[userRoom[session["user"]]]["banned"] = []
                emit("message", [rooms[userRoom[session["user"]]]["colors"][session["user"]], session["user"], message], broadcast=True, namespace='/', room=userRoom[session["user"]])
                emit("message", ["chatbot", "All bans cleared by " + session["user"]], broadcast=True, namespace='/', room=userRoom[session["user"]])

            # If command call, call chatbot
            elif "//" == message[0:2]:
                command = cb.analyze(message, session["user"])
                # If command response is to update the page style, send only to the user who requested it
                if len(command) == 2 and command[1] == "update":
                    emit("message", [rooms[userRoom[session["user"]]]["colors"][session["user"]], session["user"], message])
                    emit("message", ["chatbot", Markup(command[0])], namespace='/')
                # Otherwise, emit to all users in chat room
                else:
                    emit("message", [rooms[userRoom[session["user"]]]["colors"][session["user"]], session["user"], message], broadcast=True, namespace='/', room=userRoom[session["user"]])
                    emit("message", ["chatbot", Markup(command)], broadcast=True, namespace='/', room=userRoom[session["user"]])

            # If no special conditions, broadcast regular message to all users in room
            else:
                emit("message", [rooms[userRoom[session["user"]]]["colors"][session["user"]], session["user"], message], broadcast=True, namespace='/', room=userRoom[session["user"]])
        else:
            return redirect(url_for("login"))
    # If user disconnected and is still on tab, notify them to refresh
    except:
        emit("alert", "Session expired.  Reload page to send messages.", namespace='/')
        disconnect()

# Special case for images
@socketio.on("image")
def image(data):
    emit("imageBrodcast", [rooms[userRoom[session["user"]]]["colors"][session["user"]], session["user"], data], broadcast=True, namespace='/', room=userRoom[session["user"]])

# Runs app on deployment server
socketio.run(app, host="0.0.0.0", port=5000)
