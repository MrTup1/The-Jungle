import math
import pygame

#game variables
vertical_tile_number = 43
tileSize = 16
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
' XXXX         XX         XXXXXXXXXXXXXXXXXXXXXXX ',
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

screenWidth = 1000
screenHeight = tileSize * vertical_tile_number


screen = pygame.display.set_mode((screenWidth, screenHeight), pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.SCALED, vsync=1)
pygame.display.set_caption('DungeonDestroyers')


#Images
backgroundImg = pygame.image.load('graphics/bg.png').convert_alpha()
backgroundImg_width = backgroundImg.get_width() 
clock = pygame.time.Clock()

tiles = math.ceil((screenWidth / backgroundImg_width))