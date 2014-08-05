#-*- coding: latin1 -*-

import socket, sys, struct, threading
from header import *

class PlayerCollection(object):
	def __init__(self, game, numPlayers):
		numPlayers = 4 if numPlayers > 4 else numPlayers

		self.playersIds = [x for x in range(numPlayers)]
		self.game = game

		self.game.playersCount = len(self.playersIds)
		self.game.init(self)

	def onSet(self, row, col):
		self.game.set(row, col)

	def onExit(self, id):
		pass

class PlayerServer(PlayerCollection):
	def __init__(self, game):
		self.currentPlayerId = 0
		self.playersIds = [0]
		self.game = game
		self.game.playersCount = 1

		self.kiked = False

		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		try:
			self.socket.bind(("", PORT))
		except socket.error , msg:
			print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
			sys.exit()

		self.socket.listen(4)
		#self.socket.setblocking(1)		#Não bloquante

		self.listing = True

		self.thread = threading.Thread(target = self.listenPlayers) #tread
		self.thread.daemon = True
		self.thread.start()

		self.game.wait(self)

	def initGame(self):
		self.listing = False
		self.send("i")

		print "atual jgador:" + str(self.game.currentPlayer)
		print "quantidade jgador:" + str(self.game.playersCount)
		self.game.init()

	def onSet(self, row, col):
		if self.isPlayerTurn() != 4:
			self.set(row, col)

	#Novas Funções
	def isPlayerTurn(self):
		for player in self.playersIds:
			if player == self.game.currentPlayer:
				return player
		return 4

	def set(self, row, col):
		self.game.set(row, col)
		self.send('s', row, col)

	def onExit(self):
		self.receiving = False
	
		for player in self.playersIds:
			self.send('e', player)

		sys.exit(1)

	#Funçoes de rede
	def listenPlayers(self):
		self.conns = []
		self.threadConns = []
		self.receiving = True
		self.listing = True

		while self.listing:
			conn, addr = self.socket.accept()
			print "jogador " + str(self.game.playersCount) + " adicionado"
			self.game.playersCount += 1
			self.conns.append(conn)

			for c in self.conns:
				c.sendall(struct.pack("c i", "o", self.game.playersCount - 1))

			threadConn = threading.Thread(target = self.receive, args = (conn,)) #tread
			threadConn.daemon = True
			threadConn.start()

			self.threadConns.append(threadConn)

			if self.game.playersCount == 4:
				self.listing = False
				self.game.waiting = False

	def send(self, function, *args):
		print "enviando:", function, args
		for conn in self.conns:
			conn.sendall(struct.pack("c %s" % ("i"*len(args)), function, *args))

	def receive(self, conn):
		while self.receiving:
			data = conn.recv(1024)

			if not data: break

			print "servidor recebe: " + data
			if data[0] == "s":
				a, row, col = struct.unpack("c 2i", data)
				self.set(row, col)

			elif data[0] == "e":
				a, player = struct.unpack("c i", data)
				self.game.exit(player)
				return


class PlayerClient(PlayerCollection):
	def __init__(self, game, count = 1, host = socket.gethostname()):
		self.currentPlayerId = 0
		self.playersIds = []
		self.game = game

		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		self.socket.setblocking(1)		#Não bloquante
		#self.socket.settimeout(1)		#Definindo timeOut
		self.receiving = True

		self.socket.connect((host, PORT))

		self.thread = threading.Thread(target = self.receive) #tread
		self.thread.daemon = True
		self.thread.start()

		self.game.wait(self)

	def onSet(self, row, col):
		if self.isPlayerTurn() != 4:
			self.send("s", row, col)

	#novas funções
	def initGame(self):
		self.game.init()

	def addPlayer(self):
		self.game.playersCount += 1

	def isPlayerTurn(self):
		for player in self.playersIds:
			if player == self.game.currentPlayer:
				return player
		return 4

	def set(self, row, col):
		self.game.set(row, col)

	def onExit(self):
		self.receiving = False

		for player in self.playersIds:
			self.send('e', player)

		sys.exit(1)

	#Funçoes de rede
	def send(self, function, *args):
		self.socket.sendall(struct.pack("c %s" % ("i"*len(args)), function, *args))

	def receive(self):
		while self.receiving:
			data = self.socket.recv(1024)

			if not data: break
			print "cliente recebe: " + data
			if data:
				if data[0] == "s":
					a, row, col = struct.unpack("c 2i", data)
					self.set(row, col)

				elif data[0] == "o":
					a, player = struct.unpack("c i", data)

					self.playersIds.append(player)
					self.game.playersCount = player + 1

				elif data[0] == "i":
					self.game.waiting = False

				elif data[0] == "a":
					self.addPlayer()

				elif data[0] == "e":
					a, player = struct.unpack("c i", data)
					self.game.exit(player)
					return