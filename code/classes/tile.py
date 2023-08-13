import pygame 
from settings import *

class Tile(pygame.sprite.Sprite):
    def __init__(self, x, y , size):
      super().__init__()
      self.image = pygame.Surface((size, size))
      self.image.fill('BLACK')
      self.rect = self.image.get_rect()
      self.rect.x = x
      self.rect.y = y
    
    def update(self, scroll):
      self.rect.x += scroll
