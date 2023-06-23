import pygame

pygame.init()

screenWidth = 400
screenHeight = 600
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

#create game window
screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption('DungeonDestroyers')

#load images
backgroundImg = pygame.image.load('assets/bg.png').convert_alpha()
clock = pygame.time.Clock()

run = True
while run == True:
	#event handler
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
			
    #game logic		

	#draw background
	screen.blit(backgroundImg, (0, 0))
	
    #draw objects
	pygame.draw.rect(screen, RED, [55,50,20,25])   
	
	#update display window
	pygame.display.update()
	clock.tick(60)

	
pygame.quit()