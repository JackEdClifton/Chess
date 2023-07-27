
import socket
import json
import threading
#from src.game import Game
from src.vector2 import Vector2
from src.piece_collection import *
from src.user_conf import user_conf

class GameHandler:
	def __init__(self, sock1, addr1, sock2, addr2):
		self.sock1 = sock1
		self.addr1 = addr1
		self.sock2 = sock2
		self.addr2 = addr2

		self.is_player1_turn = True

		self.players = [
			# kings
			King(Vector2(4, 7), "./sprites/white/king.png"),
			King(Vector2(4, 0), "./sprites/black/king.png"),

			# white pieces
			Queen(Vector2(3, 7), "./sprites/white/queen.png"),
			*[Rook(Vector2(i, 7), "./sprites/white/rook.png") for i in (0, 7)],
			*[Bishop(Vector2(i, 7), "./sprites/white/bishop.png") for i in (1, 6)],
			*[Knight(Vector2(i, 7), "./sprites/white/knight.png") for i in (2, 5)],
			*[Pawn(Vector2(i, 6), "./sprites/white/pawn.png") for i in range(8)],
			
			# black pieces
			Queen(Vector2(3, 0), "./sprites/black/queen.png"),
			*[Rook(Vector2(i, 0), "./sprites/black/rook.png") for i in (0, 7)],
			*[Bishop(Vector2(i, 0), "./sprites/black/bishop.png") for i in (1, 6)],
			*[Knight(Vector2(i, 0), "./sprites/black/knight.png") for i in (2, 5)],
			*[Pawn(Vector2(i, 1), "./sprites/black/pawn.png") for i in range(8)],
		]
		
		threading.Thread(target=self.din, args=(self.sock1)).start()
		threading.Thread(target=self.din, args=(self.sock2)).start()

	def din(self, sock):
		while True:
			data = sock.recv(1024)
			# process data
			print(data)


	def dout(self):
		pass

# listen for 2 connections
# create server instance
# listen for input
# reshare board

def create_connection(sock):
	sock.listen()
	
	# listen for connections
	sock1, addr1 = sock.accept()
	sock2, addr2 = sock.accept()

	print("Accepted Clients")

	return GameHandler(sock1, addr1, sock2, addr2)


def play_game(conn):
	while True:
		data = conn.conn1.recv(1024)
		
	

def main():
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.bind(("0.0.0.0", user_conf["port"]))

	while True:
		game = create_connection(sock)
		threading.Thread(target=play_game, args=(game)).start()
	
main()


