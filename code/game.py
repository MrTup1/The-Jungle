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


pygame.init()

#Creating Objects
level = Level(level_0, screen)

level.setupLevel()

#game loop
run = True


while run == True:
	#event handler
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
			
	screen.fill('black')
	level.run()

	#update display window
	pygame.display.update()
	clock.tick(60)
	
pygame.quit()