
import pygame

from src.game import Game
from src.vector2 import Vector2



def main():

	# create game
	game = Game()

	# main loop
	while game.run:
		
		# draw background and board
		game.window.fill((50,50,150))
		game.handle_events()
		game.draw_grid()

		# draw sprites
		game.draw_sprites()

		pygame.display.update()


main()