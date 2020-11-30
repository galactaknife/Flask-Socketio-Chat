# Flask-Socketio-Chat

A simple web chat created using Python Flask and socket.io.  
ICS final project.

## Running the app

In order to run, install flask, flask-socketio, and flask_cors.
Can be installed by using the following commands in console.

<code>pip install flask</code>

<code>pip install flask-socketio</code>

<code>pip install flask_cors</code>

If you have python installed, you should already have pip installed.  If the pip command doesn't work, try using pip3 instead.

Then the app can run by using:

<code>python main.py</code>

## Deploying the app

After running the app by using <code>python main.py</code>. the app will deploy on a Werkzeug production server.  Visit <code>0.0.0.0:5000</code> to view the chat locally.  
This will be local and only accessible by you. 
If you want to deploy it to others temporarily, I recommend using <a href="https://ngrok.com">ngrok</a>.

You also should install eventlet or gevent and gevent-websocket to run it because the Werkzeug production server should only be used for development.
I personally use gevent/gevent-websocket.

They can be installed by using the following commands in console:

<code>pip install eventlet</code>

<b>OR</b>

<code>pip install gevent</code>

<code>pip install gevent-websocket</code>

Then run the app by using <code>python main.py</code> and it should use eventlet or gevent, whichever is installed.

## Miscellaneous

You can change the Admin password on line 66 of main.py by changing "admin password" to whatever password you would like.
