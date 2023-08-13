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


pygame.init()

#Creating Objects
level = Level(levelMap, screen)

level.setupLevel()

#game loop
run = True


while run == True:
	#event handler
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
			
  #game logic		

	#scroll background
	scroll = level.scroll_x()
	scroll2 = scroll * 1.1
	bgScroll += scroll2

	for i in range(10000):
		draw_bg(bgScroll, i, backgroundImg_width)
	platform_group.update(scroll)

  #draw objects
	#platform_group.draw(screen)
	level.draw()

	#update display window
	pygame.display.update()
	clock.tick(60)
	print(screenHeight)
	
pygame.quit()