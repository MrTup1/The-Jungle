import pygame
import time
import math

pygame.init()

screenWidth = 2000
screenHeight = 600

#create game window
screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption('DungeonDestroyers')

#load images
backgroundImg = pygame.image.load('assets/bg.png').convert_alpha()
backgroundImg_width = backgroundImg.get_width() 
playerImg = pygame.image.load('assets/jump.png').convert_alpha()
clock = pygame.time.Clock()


#variables
scroll = 0
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GRAVITY = 0.4
tiles = math.ceil((screenWidth / backgroundImg_width))
print(tiles)

#classes
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
		dx = 0
		dy = 0
		self.vel_y += GRAVITY
		key = pygame.key.get_pressed()
		if key[pygame.K_LEFT] or key[pygame.K_a]: 
			dx = -5
		if key[pygame.K_RIGHT] or key[pygame.K_d]:
			dx = 5
		if self.landed == False:
			pass 
		else: 			
			if key[pygame.K_w] or key[pygame.K_UP]:
					self.landed = False
					self.vel_y = -12
					self.start = time.time()	

		dy += self.vel_y

		if (self.rect.left +dx <0 or self.rect.right + dx >= screenWidth):
			screen.blit(backgroundImg, (screenWidth , 0))
			dx =0

		if self.rect.bottom +dy > screenHeight:
			self.landed = True
			dy = 0

		self.rect.x += dx 
		self.rect.y +=dy


	def draw(self):
		screen.blit(self.image, (self.rect.x - 6, self.rect.y-4))
		pygame.draw.rect(screen, RED, self.rect, 2)


#Creating Objects
player1 = Player(screenWidth // 2, screenHeight -50)

run = True
while run == True:
	#event handler
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
			
  #game logic		
	player1.move()
	#images
	for i in range(tiles):
		screen.blit(backgroundImg, (i * backgroundImg_width, 0))
	
	#scroll background

  #draw objects
	player1.draw()

	#update display window
	pygame.display.update()
	clock.tick(120)
	
pygame.quit()