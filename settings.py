import math
import pygame

#game variables
scroll = 8
bgScroll = 0
temp = 0
platform_group = pygame.sprite.Group()
levelMap = [
'                            ',
'                            ',
'                            ',
' XX    XXX            XX    ',
' XX P                        ',
' XXXX         XX         XX ',
' XXXX       XX              ',
' XX    X  XXXX    XX  XX    ',
'       X  XXXX    XX  XXX   ',
'    XXXX  XXXXXX  XX  XXXX  ',
'XXXXXXXX  XXXXXX  XX  XXXX  ']

#constants
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GRAVITY = 0.8	
MAX_PLATFORMS = 5
SCROLL_THRESH = 200
tileSize = 64

screenWidth = 500
screenHeight = len(levelMap) * tileSize



screen = pygame.display.set_mode((screenWidth, screenHeight), pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.SCALED, vsync=1)
pygame.display.set_caption('DungeonDestroyers')


#Images
backgroundImg = pygame.image.load('assets/bg.png').convert_alpha()
backgroundImg_width = backgroundImg.get_width() 
playerImg = pygame.image.load('assets/jump.png').convert_alpha()
platformImg = pygame.image.load('assets/wood.png').convert_alpha()
clock = pygame.time.Clock()

tiles = math.ceil((screenWidth / backgroundImg_width))