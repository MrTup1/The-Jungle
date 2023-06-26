import pygame
import time
import math
import random

pygame.init()
 
screenWidth = 1000
screenHeight = 600

#create game window
screen = pygame.display.set_mode((screenWidth, screenHeight), pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.SCALED, vsync=1)
pygame.display.set_caption('DungeonDestroyers')

#load images
backgroundImg = pygame.image.load('assets/bg.png').convert_alpha()
backgroundImg_width = backgroundImg.get_width() 
playerImg = pygame.image.load('assets/jump.png').convert_alpha()
platformImg = pygame.image.load('assets/wood.png').convert_alpha()
clock = pygame.time.Clock()


#variables
scroll = 0
bgScroll = 0
temp = 0

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GRAVITY = 0.8	
MAX_PLATFORMS = 5
SCROLL_THRESH = 11
tiles = math.ceil((screenWidth / backgroundImg_width))

#functionsd
def draw_bg(bgScroll):
	screen.blit(backgroundImg, (0 + bgScroll, 0))

 

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

		if self.rect.bottom +dy > screenHeight:
			self.rect.bottom = screenHeight
			self.landed = True
			dy = 0

		self.rect.x += dx + scroll
		self.rect.y +=dy

		return scroll
		
	def draw(self):
		screen.blit(self.image, (self.rect.x - 6, self.rect.y-4))
		pygame.draw.rect(screen, RED, self.rect, 2)

class Platform(pygame.sprite.Sprite):
	def __init__(self, x, y, width): 
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.transform.scale(platformImg, (width, 10))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y

	def update(self, scroll):
		self.rect.x += scroll

#Creating Objects
player1 = Player(screenWidth // 2, screenHeight -50)

#create sprite groups
platform_group = pygame.sprite.Group()

for p in range(MAX_PLATFORMS):
	platformWidth = random.randint(100,120)
	platformX = random.randint(int(temp), 3* screenWidth)
	platformY = random.randint(screenHeight - 320, screenHeight - 60)
	platform = Platform(platformX, platformY, platformWidth)
	platform_group.add(platform)
	temp += platformWidth * 1.2

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
	for i in range(tiles):
		screen.blit(backgroundImg, (i* backgroundImg_width, 0))
	platform_group.update(scroll)

  #draw objects
	player1.draw()
	platform_group.draw(screen)
	#pygame.draw.line(screen, RED, (screenWidth-SCROLL_THRESH, 0) , (screenWidth-SCROLL_THRESH, screenHeight))



	#update display window
	pygame.display.update()
	clock.tick(60)
	
pygame.quit()