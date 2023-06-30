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
player1 = Player(screenWidth // 2, screenHeight -50)
level = Level(levelMap, screen)

#create sprite groups
for p in range(MAX_PLATFORMS):
	platformWidth = random.randint(100,120)
	platformX = random.randint(int(temp), 3* screenWidth)
	platformY = random.randint(screenHeight - 320, screenHeight - 60)
	platform = Platform(platformX, platformY, platformWidth)
	platform_group.add(platform)
	temp += platformWidth * 1.2


level.setupLevel()
#game loop
run = True

while run == True:
	#event handler
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
			
  #game logic		
	scroll = player1.move()

	#scroll background
	scroll2 = scroll * 1.1
	bgScroll += scroll2
	for i in range(10000):
		draw_bg(bgScroll, i, backgroundImg_width)
	platform_group.update(scroll)

  #draw objects
	player1.draw()
	platform_group.draw(screen)
	level.draw(scroll)

	#update display window
	pygame.display.update()
	clock.tick(60)
	
pygame.quit()