#-*- coding: latin1 -*-

import sys, pygame

from Game import *
from PlayerConection import *
from header import *

def main(args):
	pygame.init()

	screen = pygame.display.set_mode((W_WIDTH, W_HEIGHT))
	pygame.display.set_caption('Connector Line')

	game = Game(screen)


	if len(sys.argv) > 1 and sys.argv[1] == "server":
	 	PlayerServer(game)

	elif len(sys.argv) > 1 and sys.argv[1] == "client":

		if len(sys.argv) > 2:
			PlayerClient(game, sys.argv[2])
		else:
			PlayerClient(game)

	elif len(sys.argv) > 1 and sys.argv[1].isdigit():
		PlayerCollection(game, int(sys.argv[1]))

	else:
		PlayerCollection(game, 2)

if __name__ == '__main__':
	main(sys.argv)