import pygame
import time
import math
import random
from settings import *

class Platform(pygame.sprite.Sprite):
	def __init__(self, x, y, width): 
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.transform.scale(platformImg, (width, 10))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y

	def update(self, scroll):
		self.rect.x += scroll