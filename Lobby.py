#-*- coding: latin1 -*-

import pygame, sys, math
from header import *

class Lobby(object):
	def __init__(self, screen):
		self.screen = screen
		self.clock = pygame.time.Clock()
		self.time = 0

		self.interface = LobbyMode(self.screen);

		while True:
			self.loop()

	def loop(self):
		dt = self.clock.tick(30)
		self.time += dt / 1000.

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
		
		self.interface.loop(dt)
		pygame.display.flip()

class LobbyMode(pygame.Surface):

	def __init__(self, screen):
		self.screen = screen
		super(LobbyMode, self).__init__((W_WIDTH, W_HEIGHT))

		self.button = pygame.sprite.Group()

		creatButton = LobbyButton("Creat a Lobby", self.button)
		creatButton.center = (160, 240)
		joinButton = LobbyButton("Join in a Lobby", self.button)
		joinButton.center = (480, 240)

	def loop(self, dt):
		self.fill((0, 0, 0))
		
		self.button.update()
		self.button.draw(self.screen)

		#self.blit(self.screen)

class LobbyButton(pygame.sprite.Sprite):

	def __init__(self, text, *groups):
		super(LobbyButton, self).__init__(*groups)
		self.text = text

		self.center = (320, 240)

	def update(self):
		#draw text
		self.basicFont = pygame.font.SysFont("Aerial", 22)
		textRender = self.basicFont.render(self.text, True, C_WHITE)

		self.image = textRender
		self.rect = textRender.get_rect(center= self.center)