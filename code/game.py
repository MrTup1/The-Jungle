import pygame
import time
import math
import random
from settings import *
from classes.platform import Platform
from classes.player import Player
from classes.tile import Tile
from classes.level import Level
from functions.background import *
from functions.support import *
from game_data import *
from overworld import Overworld

class Game: 
	def __init__(self):
		self.maxLevel = 3
		self.overworld = Overworld(0, self.maxLevel, screen)
		self.overworld.setupNodes()
	
	def run(self):
		self.overworld.run()

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
	game.run()

	#update display window
	pygame.display.update()
	clock.tick(60)
	
pygame.quit()