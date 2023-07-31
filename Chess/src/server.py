
import socket
import json
import threading
import pickle
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
		threading.Thread(target=self.gameloop).start()

	def gameloop(self):
		while True:

			if self.is_player1_turn: sock = self.sock1
			else: sock = self.sock2
			
			data = sock.recv(1024)
			
			# tell other player
			if self.is_player1_turn:
				sock = self.sock2
			else:
				sock = self.sock1

			# send response
			if data:
				sock.sendall(data)
			else:
				sock.close()
				break

			self.is_player1_turn = not self.is_player1_turn


def create_connection(sock):
	sock.listen()
	
	# listen for connections
	sock1, addr1 = sock.accept()
	sock1.sendall(b"1")

	sock2, addr2 = sock.accept()
	sock2.sendall(b"0")

	print("Accepted Clients")

	return GameHandler(sock1, addr1, sock2, addr2)
		
	

def main():
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.bind(("0.0.0.0", user_conf["port"]))

	games = []

	while True:
		games.append(create_connection(sock))
	
main()


