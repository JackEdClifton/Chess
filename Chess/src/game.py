
import pygame
import winsound
import requests
import socket
import threading
import pickle
from src.vector2 import Vector2
from src.piece_collection import *
from src.user_conf import user_conf

class Game:
	square_size = 75
	grid_pos = Vector2(10, 10)

	# colours for squares
	board_colours = [
		(240, 230, 200), # light
		(200, 170, 120), # dark
		(255, 245, 215), # light hover - old
		(215, 185, 135), # dark hover - old
		(255, 250, 225), # light hover
		(235, 195, 145), # dark hover
	]

	def __init__(self):
		self.run = True
		self.window = pygame.display.set_mode((620, 620))
		self.is_player1_turn = True
		self.active_sprite = None
		self.highlight_moves = []
		self.unprocessed_online_move = None

		self.players = [
			# kings
			King(Vector2(4, 7), "./sprites/white/king.png"),
			King(Vector2(4, 0), "./sprites/black/king.png"),

			# white pieces
			Queen(Vector2(3, 7), "./sprites/white/queen.png"),
			*[Rook(Vector2(i, 7), "./sprites/white/rook.png") for i in (0, 7)],
			*[Bishop(Vector2(i, 7), "./sprites/white/bishop.png") for i in (2, 5)],
			*[Knight(Vector2(i, 7), "./sprites/white/knight.png") for i in (1, 6)],
			*[Pawn(Vector2(i, 6), "./sprites/white/pawn.png") for i in range(8)],
			
			# black pieces
			Queen(Vector2(3, 0), "./sprites/black/queen.png"),
			*[Rook(Vector2(i, 0), "./sprites/black/rook.png") for i in (0, 7)],
			*[Bishop(Vector2(i, 0), "./sprites/black/bishop.png") for i in (2, 5)],
			*[Knight(Vector2(i, 0), "./sprites/black/knight.png") for i in (1, 6)],
			*[Pawn(Vector2(i, 1), "./sprites/black/pawn.png") for i in range(8)],
		]

		title = "Offline"

		# init conn
		if user_conf["online-mode"] == "server":
			self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.sock.connect((user_conf["server-ip"], user_conf["port"]))
			self.client_player = int(self.sock.recv(1024).decode())
			threading.Thread(target=self.din).start()

			title = "Your Turn" if self.client_player == self.is_player1_turn else "Opponents Turn"
		pygame.display.set_caption("Chess - " + title)

	# handle network input
	def din(self):
		while True:
			data = self.sock.recv(1024).decode()

			if not data:
				self.sock.close()
				self.run = False

			# process data
			start_pos = data[:2]
			end_pos = data[2:]

			# kill other sprite (if exists)
			kill_target = self.get_from_posision(Vector2(*(int(i) for i in list(end_pos))))
			if kill_target != None:
				self.players.remove(kill_target)

			# move piece
			for player in self.players:
				if player.pos == Vector2(*(int(i) for i in list(start_pos))):
					player.move_to(Vector2(*(int(i) for i in list(end_pos))))
					self.is_player1_turn = not self.is_player1_turn
					
					title = "Your Turn" if self.client_player == self.is_player1_turn else "Opponents Turn"
					pygame.display.set_caption("Chess - " + title)


	# handle events and input
	def handle_events(self):

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.run = False

			if event.type == pygame.MOUSEBUTTONDOWN:

				# ignore inputs if other players turn
				if user_conf["online-mode"] == "server":
					if self.client_player != self.is_player1_turn: continue


				# check if player is moving a sprite
				if self.active_sprite != None:
					for move in self.highlight_moves:
						move_pos = Game.grid_pos + move * Vector2(75,75)
						if pygame.Rect(move_pos.x, move_pos.y, Game.square_size, Game.square_size).collidepoint(event.pos):

							# get active sprite
							for sprite in self.players:

								# move sprite
								if id(sprite) == self.active_sprite:

									# kill other sprite (if exists)
									kill_target = self.get_from_posision(move)
									if kill_target != None:
										self.players.remove(kill_target)

									# move the sprite
									sprite_starting_pos = sprite.pos
									sprite.move_to(move)
									self.active_sprite = None
									self.highlight_moves = []

									# check friendly check (moving a blocker)
									player_in_check = 0
									for each_sprite in self.players:
										for move in each_sprite.get_moves(self):
											if move == self.players[0].pos: player_in_check = 1
											if move == self.players[1].pos: player_in_check = 2

									if 1 + (not self.is_player1_turn) == player_in_check:
										sprite.undo_move()
										winsound.PlaySound("./audio/mixkit-wrong-electricity-buzz-955.wav", winsound.SND_FILENAME)

										# if a sprite was removed during an illegal move, replace it
										if kill_target != None:
											self.players.append(kill_target)

										return

									# move is valid, complete transaction
									self.is_player1_turn = not self.is_player1_turn
									title = "Your Turn" if self.client_player == self.is_player1_turn else "Opponents Turn"
									pygame.display.set_caption("Chess - " + title)

									# send move to host
									self.sock.sendall(
										str("".join((str(sprite_starting_pos.x), str(sprite_starting_pos.y), str(sprite.pos.x), str(sprite.pos.y)))).encode()
									)

									return
									


				# check if player has clicked a sprite
				for sprite in self.players:

					# ignore if sprite is on other team
					if sprite.is_white != self.is_player1_turn:
						continue

					sprite_pos = Game.grid_pos + sprite.pos * Vector2(75,75)
						
					if pygame.Rect(sprite_pos.x, sprite_pos.y, Game.square_size, Game.square_size).collidepoint(event.pos):

						# set or remove as active sprite
						self.active_sprite = id(sprite) if self.active_sprite != id(sprite) else None
							
						# get highlighted squares for active sprite
						self.highlight_moves = []
						for sprite in self.players:
							if self.active_sprite == id(sprite):
								self.highlight_moves = sprite.get_moves(self)



	# draw game board
	def draw_grid(self) -> None:

		# copy to local object
		square_pos = Game.grid_pos.get_copy()

		# iterate through grid
		for y in range(8):
			for x in range(8):

				# get base square colour
				is_dark_square = (x+y) % 2
				is_highlighted_square = False

				# get bound of square
				square_rect = (square_pos.x, square_pos.y, Game.square_size, Game.square_size)
			
				# use highlighted colour if mouse is over current square
				if pygame.Rect(square_rect).collidepoint(*pygame.mouse.get_pos()):
					is_highlighted_square = True

				# use highlighted colour if the active sprite can move to this square
				if Vector2(x,y) in self.highlight_moves:
					is_highlighted_square = True

				# draw square
				pygame.draw.rect(self.window, self.board_colours[is_dark_square + is_highlighted_square*2], square_rect)
				if is_highlighted_square:
					pygame.draw.rect(self.window, (0,0,0), (square_pos.x+1, square_pos.y+1, Game.square_size-2, Game.square_size-2), 3)

				# increment to next square
				square_pos.x += Game.square_size
			
			# move to start of next row
			square_pos.x -= Game.square_size * 8
			square_pos.y += Game.square_size

			
	# draw all sprites
	def draw_sprites(self) -> None:
		for sprite in self.players:
			pos = Game.grid_pos + sprite.pos * Vector2(Game.square_size, Game.square_size)
			self.window.blit(sprite.surface, pos.get_tuple())
				

	# get piece at position
	def get_from_posision(self, target_pos: Vector2):
		for sprite in self.players:
			if sprite.pos == target_pos:
				return sprite
		return None

