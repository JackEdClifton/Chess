
import flask
import os

from src.vector2 import Vector2
from src.user_conf import user_conf

# create webserver
app = flask.Flask(__name__)

# might delete
@app.route("/is-online")
def is_online():
	return "yes"

# for client to get the hosts move
@app.route("/get-move")
def get_move():
	return ""

# host waits for client to send their move
@app.route("/send-move")
def send_move():
	data = flask.request.args.get("data")
	start_pos = data[:2]
	end_pos = data[2:]
	print(start_pos)
	print(end_pos)
	return ""

#if user_conf["online-mode"] == "server" or __name__ == "__main__":
	#app.run("0.0.0.0", user_conf["port"])

