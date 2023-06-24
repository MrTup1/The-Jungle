import pygame

pygame.init()

screenWidth = 400
screenHeight = 600

#colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

#create game window
screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption('DungeonDestroyers')

#load images
backgroundImg = pygame.image.load('assets/bg.png').convert_alpha()
playerImg = pygame.image.load('assets/jump.png').convert_alpha()
clock = pygame.time.Clock()

#classes
class Player():
	def __init__(self,x,y):
		self.image = pygame.transform.scale(playerImg, (50,50)) 
		self.width = 38
		self.height = 46
		self.rect = pygame.Rect(0, 0, self.width, self.height)
		self.rect.center = (x,y)
	
	def move(self):
		key = pygame.key.get_pressed()
		if key[pygame.K_a]: 
			self.rect.x -= 10
		if key[pygame.K_d]:
			self.rect.x +=10

	def draw(self):
		screen.blit(self.image, (self.rect.x - 6, self.rect.y-4))
		pygame.draw.rect(screen, RED, self.rect, 2)

player1 = Player(screenWidth // 2, screenHeight //2)

run = True
while run == True:
	#event handler
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
			
  #game logic		
	player1.move()
	#images
	screen.blit(backgroundImg, (0, 0))
	
  #draw objects
	player1.draw()

	#update display window
	pygame.display.update()
	clock.tick(60)
	
pygame.quit()