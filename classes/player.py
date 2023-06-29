import pygame
import time
import math
import random
from settings import *

class Player():
	def __init__(self,x,y):
		self.image = pygame.transform.scale(playerImg, (50,50)) 
		self.width = 38
		self.height = 46
		self.vel_y = 0
		self.start = 0
		self.end = 0
		self.landed = False
		self.rect = pygame.Rect(0, 0, self.width, self.height)
		self.rect.center = (x,y)
	
	def move(self):
		scroll = 0
		dx = 0
		dy = 0
		self.vel_y += GRAVITY
		key = pygame.key.get_pressed()

		if key[pygame.K_LEFT] or key[pygame.K_a]: 
			dx = -10
		if key[pygame.K_RIGHT] or key[pygame.K_d]:
			dx = 10
		if self.landed == False:
			pass 
		else: 			
			if key[pygame.K_w] or key[pygame.K_UP]:
					self.landed = False
					self.vel_y = -20
					self.start = time.time()	
		dy += self.vel_y
		#check collision with platforms
		for platform in platform_group:
			if platform.rect.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
				if self.rect.bottom < platform.rect.centery:
					if self.vel_y > 0:  
						self.rect.bottom = platform.rect.top
						self.landed = True
						self.vel_y = 0
						dy = 0

		#check collision with ground and side
		if (self.rect.left +dx <0 or self.rect.right + dx >= screenWidth):
			screen.blit(backgroundImg, (screenWidth , 0))
			dx =0

		#check if player moved pass scroll threshold
		if self.rect.right >= screenWidth - SCROLL_THRESH:
			if dx > 0:
				scroll = -dx
		if self.rect.left <= SCROLL_THRESH:
			if dx < 0: 
				scroll = dx

		if self.rect.bottom +dy > screenHeight:
			self.rect.bottom = screenHeight
			self.landed = True
			dy = 0

		if dx > 0:
			self.rect.x += dx + scroll
		else: 
			self.rect.x += dx - scroll
			scroll = scroll * -1
		self.rect.y +=dy

		return scroll
		
	def draw(self):
		screen.blit(self.image, (self.rect.x - 6, self.rect.y-4))
		pygame.draw.rect(screen, RED, self.rect, 2)