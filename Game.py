#-*- coding: latin1 -*-

import pygame, sys, math

from PlayerConection import *
from header import *

class Game(object):
	def __init__(self, screen):
		self.screen = screen
		self.playersCount = 0
		self.currentPlayer = 0
		self.waiting = False
		self.historicPoints = [4, 0]

		self.table = [[None for x in range(NUM_COLUM)] for x in range(NUM_LINES)]

	def wait(self, playerCollection):
		self.playerCollection = playerCollection
		self.waiting = True

		while self.waiting:
			for event in pygame.event.get():
				if event.type == pygame.MOUSEBUTTONUP and type(self.playerCollection) == PlayerServer:
					self.waiting = False

		print "iniciando jogo"
		playerCollection.initGame()

	def init(self, playerCollection = None):

		self.players = [Player(x) for x in range(self.playersCount)]

		if playerCollection:
			self.playerCollection = playerCollection

		self.cubes = pygame.sprite.Group()
		self.lines = pygame.sprite.Group()
		self.scores = pygame.sprite.Group()
		self.setLines = pygame.sprite.OrderedUpdates()

		self.initLines()
		self.clock = pygame.time.Clock()

		for player in self.players:
			Score(player, self.scores)

		self.time = 0
		while True:
			self.loop()

	def exit(self, playerId):
		sys.exit(1)

	def loop(self):
		dt = self.clock.tick(30)
		self.time += dt / 1000.

		#print str(self.time) + "s"

		self.screen.fill((0, 0, 0))

		if self.events():
			return

		self.lines.update()
		self.scores.update(dt / 1000.)
		self.setLines.update()
		self.cubes.update(dt / 1000.)

		self.setLines.draw(self.screen)
		self.lines.draw(self.screen)
		self.cubes.draw(self.screen)
		self.scores.draw(self.screen)

		pygame.display.flip()

	def events(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.playerCollection.onExit()
				return True

			if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
				self.playerCollection.onExit()
				return True

			if event.type == pygame.MOUSEBUTTONUP:
				self.onClick()
				return False

	def onClick(self):
		mouseSprite = pygame.sprite.Sprite()
		mouseSprite.rect = pygame.Rect(pygame.mouse.get_pos(), (1, 1))

		colidedLine = pygame.sprite.spritecollideany(mouseSprite, self.lines)
		if colidedLine != None:
			self.playerCollection.onSet(colidedLine.row, colidedLine.col)

	def set(self, row, col):
		colidedLine = self.table[row][col]
		player = self.players[self.currentPlayer]

		pos = colidedLine.setMaster(player)

		if not self.checkBox(player, *pos):
			self.historicPoints = [4, 0]
			self.nextPlayer()

		self.setLines.add(colidedLine)
		self.lines.remove(colidedLine)

		if len(self.lines.sprites()) == 1:
			lastSprite = self.lines.sprites()[0]
			self.set(lastSprite.row, lastSprite.col)
			finishinGame()

	def checkBox(self, player, row, col):
		check = False

		if row % 2:
			if col > 0 and self.table[row][col - 1].hadMaster():
				if self.table[row - 1][col - 1].hadMaster() and self.table[row + 1][col - 1].hadMaster():

					# self.table[row][col - 1].setMaster(player)
					# self.table[row - 1][col - 1].setMaster(player)
					# self.table[row + 1][col - 1].setMaster(player)

					Cube(player, row - 1, col - 1, self.cubes)
					self.givePlayerPoints()
					check = True

			if col < NUM_COLUM -1 and self.table[row][col + 1].hadMaster():
				if self.table[row - 1][col].hadMaster() and self.table[row + 1][col].hadMaster():

					# self.table[row][col + 1].setMaster(player)
					# self.table[row - 1][col].setMaster(player)
					# self.table[row + 1][col].setMaster(player)

					Cube(player, row - 1, col, self.cubes)
					self.givePlayerPoints()
					check = True
		else:
			if row > 0 and self.table[row -2][col].hadMaster():
				if self.table[row -1][col].hadMaster() and self.table[row -1][col +1].hadMaster():

					# self.table[row -2][col].setMaster(player)
					# self.table[row -1][col].setMaster(player)
					# self.table[row -1][col +1].setMaster(player)

					Cube(player, row - 2, col, self.cubes)
					self.givePlayerPoints()
					check = True

			if row < NUM_LINES -1 and self.table[row +2][col].hadMaster():
				if self.table[row +1][col].hadMaster() and self.table[row +1][col +1].hadMaster():

					# self.table[row +2][col].setMaster(player)
					# self.table[row +1][col].setMaster(player)
					# self.table[row +1][col +1].setMaster(player)

					Cube(player, row, col, self.cubes)
					self.givePlayerPoints()
					check = True

		return check

	def nextPlayer(self):
		self.currentPlayer = (self.currentPlayer + 1) % self.playersCount

	def givePlayerPoints(self):
		player = self.players[self.currentPlayer]

		if self.historicPoints[0] == player.id:
			player.score += 20 + 5 * self.historicPoints[1]
			self.historicPoints[1] += 1

		else:
			player.score += 20
			self.historicPoints = [player.id, 1]

	def finishinGame(self):
		winPlayerList = [self.players[0]]
		for player in self.players[1:]:

			if winPlayerList[0].score < player.score:
				winPlayerList = [player]

			elif winPlayerList[0].score == player.score:
				winPlayerList.append(player)

		print "%s %s" % ("e".join([str(player) for player in winPlayerList]),
						"vencedor" if len(winPlayerList) > 1 else "vencedores")
	#init alciliar
	def initLines(self):
		for l in range(NUM_LINES / 2):
			for c in range(NUM_COLUM - 1):
				Line("H", l, c, self.table, self.lines)
				Line("V", l, c, self.table, self.lines)

			Line("V", l, NUM_COLUM - 1, self.table, self.lines)

		for c in range(NUM_COLUM - 1):
			Line("H", math.ceil(NUM_LINES / 2), c, self.table, self.lines)

class Line(pygame.sprite.Sprite):
	def __init__(self, direction, r, c, table, *groups):
		super(Line, self).__init__(*groups)

		x = LEFT_MARGIN + c * BLOCK_SIZE
		y = TOP_MARGIN + r * BLOCK_SIZE

		if direction == "H":
			(w, h, x, y, r) = (BLOCK_SIZE + 4, 4, x - 2, y - 2, r * 2)

		else:
			(w, h, x, y, r) = (4, BLOCK_SIZE + 4, x - 2, y - 2, r * 2 + 1)

		self.master = 4
		self.row = int(r)
		self.col = int(c)

		self.color = C_GRAY
		self.image = pygame.Surface((w, h), flags = pygame.SRCALPHA)
		self.image.fill(self.color)

		self.rect = self.image.get_rect(x = x, y = y)

		table[self.row][self.col] = self

	def hadMaster(self):
		return self.master != 4

	def setMaster(self, player):
		self.master = player.id
		self.color = colorDefine[player.id + 1]

		return (self.row, self.col)

	def update(self):
		self.image.fill(self.color)

class Cube(pygame.sprite.Sprite):
	def __init__(self, player, l, c, *groups):
		super(Cube, self).__init__(*groups)

		x = LEFT_MARGIN + c * BLOCK_SIZE + 2
		y = TOP_MARGIN + math.floor(l / 2) * BLOCK_SIZE + 2

		self.image = pygame.Surface((BLOCK_SIZE - 4, BLOCK_SIZE - 4))
		#self.image.fill(colorDefine[player.id + 1])

		self.rect = self.image.get_rect(x = x, y = y)
		self.update = self.onAnimation
		self.width = 1
		self.color = colorDefine[player.id + 1]
		self.time = 0

	def offAnimation(self, dt):
		pass

	def onAnimation(self, dt):
		# def linearTween (t, b, c, d):
		# 	return c*t/d + b;
		self.width = math.linearTween(self.time, 1, BLOCK_SIZE - 4, 0.5)
		self.time += dt

		self.image.fill((0,0,0))
		pygame.draw.rect(self.image, self.color, self.image.get_rect(x = 0, y = 0), int(self.width)) #width = int(math.floor(self.width)))

		#if self.time - dt >= totalTime:
		#	self.update = self.offAnimation


class Score(pygame.sprite.Sprite):
	def __init__(self, player, *groups):
		super(Score, self).__init__(*groups)

		self.player = player
		self.lastScore = 0

		x, y = self.defPorsition(player.id)
		self.image = pygame.Surface((100, 50))
		self.rect = self.image.get_rect(x = x, y = y)

		self.basicFont = pygame.font.SysFont("Aerial", 22)
		self.drawText()

	def update(self, dt):
		if self.lastScore != self.player.score:

			if self.lastScore + dt * 50 >= self.player.score:
				self.lastScore = self.player.score
			else:
				self.lastScore += dt * 50

			self.image.fill((0, 0, 0))
			self.drawText()
			#self.lastScore = self.player.score

	def drawText(self):
		text = self.basicFont.render("%04d" % self.lastScore, True, C_WHITE)
		textRect = text.get_rect()
		textRect.centery = 25

		if self.rect.x == W_WIDTH - LEFT_MARGIN - 100:
			textRect.right = 100

		self.image.blit(text, textRect)

	def defPorsition(self, id):
		case = {0: (LEFT_MARGIN, 10),
				1: (W_WIDTH - LEFT_MARGIN - 100, 10),
				2: (LEFT_MARGIN, W_HEIGHT - 10 - 50),
				3: (W_WIDTH - LEFT_MARGIN - 100, W_HEIGHT - 10 - 50)}

		return case[id]

class Player(object):
	def __init__(self, id):
		self.score = 0
		self.id = id

	def __str__(self):
		return "Jogador %d" % (self.id + 1)

def linearTween(t, b, c, d):
	t = 1 if t > d else t/d
	return c*t + b;

def easeInCirc(t, b, c, d):
	t = 1 if t > d else t/d
	return -c * (math.sqrt(1 - t * t) - 1) + b

def easeOutBounce(t, b, c, d):
	t = 1 if t > d else t / d
	if (t) < (1/2.75):
		return c*(7.5625*t*t) + b

	elif t < (2/2.75):
		t -= (1.5/2.75)
		return c*(7.5625*t)*t + .75 + b

	elif t < (2.5/2.75):
		t -= (2.25/2.75)
		return c*(7.5625*t)*t + .9375 + b;
	else:
		t -= (2.625/2.75)
		return c*(7.5625*t)*t + .984375 + b;

math.easeInCirc = easeInCirc
math.linearTween = linearTween
math.easeOutBounce = easeOutBounce
