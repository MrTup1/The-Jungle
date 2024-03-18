import pygame
import time
import math
import random
from settings import *
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
		self.status = 'overworld'
		self.maxHealth = 5	
		self.currentHealth = 5
		self.coins = 0

		self.ui = UI(screen)

	def createLevel(self, currentLevel): #Create a level instance
		self.level = Level(currentLevel, screen, self.createOverworld, self.updateCoins, self.changeHealth)
		self.status = 'level'

	def createOverworld(self, currentLevel, newMaxLevel): #Create an overworld instance
		if newMaxLevel > self.maxLevel:
			self.maxLevel = newMaxLevel
		self.overworld = Overworld(currentLevel, self.maxLevel, screen, self.createLevel, self.createStart)
		self.status = 'overworld'
	
	def createStart(self, currentLevel): #Create the start menu UI
		self.start = Start(currentLevel, screen, self.createOverworld)
		self.status = 'start'

	def changeHealth(self, amount): #Change the health of the player 
		self.currentHealth += amount

	def updateCoins(self, amount): #Change total coins collected
		self.coins += amount
	
	def gameOver(self): #Show game over UI and reset attributes of all classes
		keys = pygame.key.get_pressed()
		if self.currentHealth <= 0: #Check if player has no health left
			self.level.dead = True #Set dead status to true
			self.ui.drawBlackOverlay() 
			self.ui.showGameOver()
			if keys[pygame.K_RETURN]: #Wait for player to press "Enter"
				self.currentHealth = 5
				self.coins = 0
				self.maxLevel = 0
				self.status = 'overworld'
				self.overworld = Overworld(0, self.maxLevel, screen, self.createLevel, self.createStart)

	def getQuit(self): #Obtain game status if the player has pressed the quit button in the start menu UI
		if self.start.getQuit():
			return True

	def run(self):
		if self.status == 'overworld': #Displays corresponding elements depending on the status attribute
			self.overworld.run()
		elif self.status == 'start':
			self.start.run()
		else: 
			self.level.run() #Run the level class
			self.gameOver()
			if self.level.dead == False and self.level.completedLevel == False: #Check if player is still alive and playing the game
				self.ui.showHealth(self.currentHealth, 5)
				self.ui.showCoins(self.coins)
pygame.init() 

#game loop
run = True
game = Game()


while run == True: #Main game loop
	#event handler
	for event in pygame.event.get(): #Check if player pressed close window(top right button) in Windows or MacOS
		if event.type == pygame.QUIT:
			run = False
			
	if game.getQuit():
		run = False
	game.run()

	#update display window
	pygame.display.update()
	clock.tick(60) #Updates game 60 times a second
	
pygame.quit()