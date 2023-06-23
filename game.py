import pygame 

pygame.init()

#variables
BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)
GREEN    = (   0, 255,   0)
RED      = ( 255,   0,   0)
BLUE     = (   0,   0, 255)

#game window
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Dungeon Destroyers')
clock = pygame.time.Clock()

run = True
while run == True:
    #event handler for key strokes
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False 

    #clears screen and set background        
    screen.fill(WHITE)

    #drawing code
    pygame.draw.rect(screen, RED, [55, 50, 20, 25], 0)
    #updates screen with drawing code
    pygame.display.flip()

    #60 updates a second
    clock.tick(60)
pygame.quit()