import pygame
import time
import math
import random
from settings import *
from classes.platform import Platform
from classes.player import Player
from classes.tile import Tile
from classes.level import Level, NewLevel
from functions.background import *
from functions.support import *
from game_data import *
from overworld import Overworld

class Game: 
	def __init__(self):
		self.maxLevel = 2
		self.overworld = Overworld(1, self.maxLevel, screen, self.createLevel)
		self.status = 'overworld'

	def createLevel(self, currentLevel):
		self.level = Level(currentLevel, screen, self.createOverworld)
		self.status = 'level'

	def createOverworld(self, currentLevel, newMaxLevel):
		if newMaxLevel > self.maxLevel:
			self.maxLevel = newMaxLevel
		self.overworld = Overworld(currentLevel, self.maxLevel, screen, self.createLevel)
		self.status = 'overworld'

	def run(self):
		if self.status == 'overworld':
			self.overworld.run()
		else: 
			self.level.run()

pygame.init() 

#Creating Objects
#level = Level(level_0, screen)

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
	game.run()

	#update display window
	pygame.display.update()
	clock.tick(60)
	
pygame.quit()