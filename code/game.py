import pygame
import time
import math
import random
from settings import *
from classes.platform import Platform
from classes.player import Player
from classes.tile import Tile
from classes.level import Level
from classes.ui import UI
from classes.start import Start
from functions.background import *
from functions.support import *
from game_data import *
from overworld import Overworld

class Game: 
	def __init__(self):
		self.maxLevel = 0
		self.overworld = Overworld(0, self.maxLevel, screen, self.createLevel, self.createStart)
		self.start = Start(0, screen, self.createOverworld)
		self.status = 'start'
		self.maxHealth = 5	
		self.currentHealth = 5
		self.coins = 0

		self.ui = UI(screen)

	def createLevel(self, currentLevel):
		self.level = Level(currentLevel, screen, self.createOverworld, self.updateCoins, self.changeHealth)
		self.status = 'level'

	def createOverworld(self, currentLevel, newMaxLevel):
		if newMaxLevel > self.maxLevel:
			self.maxLevel = newMaxLevel
		self.overworld = Overworld(currentLevel, self.maxLevel, screen, self.createLevel, self.createStart)
		self.status = 'overworld'
	
	def createStart(self, currentLevel):
		self.start = Start(currentLevel, screen, self.createOverworld)
		self.status = 'start'

	def changeHealth(self, amount):
		self.currentHealth += amount

	def updateCoins(self, amount):
		self.coins += amount
	
	def gameOver(self):
		keys = pygame.key.get_pressed()
		if self.currentHealth <= 0: #If player has no health left
			self.level.dead = True #Set dead status to true
			self.ui.drawBlackOverlay() 
			self.ui.showGameOver()
			if keys[pygame.K_RETURN]: #Wait for player to press "Enter"
				self.currentHealth = 5
				self.coins = 0
				self.maxLevel = 0
				self.status = 'overworld'
				self.overworld = Overworld(0, self.maxLevel, screen, self.createLevel, self.createStart)

	def getQuit(self):
		if self.start.getQuit():
			return True

	def run(self):
		if self.status == 'overworld':
			self.overworld.run()
		elif self.status == 'start':
			self.start.run()
		else: 
			self.level.run()
			self.gameOver()
			if self.level.dead == False:
				self.ui.showHealth(self.currentHealth, 5)
				self.ui.showCoins(self.coins)
pygame.init() 

#game loop
run = True
game = Game()


while run == True:
	#event handler
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
			
	#level.run()
	screen.fill("WHITE")
	if game.getQuit():
		run = False
	game.run()

	#update display window
	pygame.display.update()
	clock.tick(60)
	
pygame.quit()