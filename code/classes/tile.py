import pygame 
from settings import *

class Tile(pygame.sprite.Sprite):
    def __init__(self, x, y, size):
      super().__init__()
      self.image = pygame.Surface((size, size))
      self.image.fill('GREEn')
      self.rect = self.image.get_rect()
      self.rect.x = x
      self.rect.y = y
    
    def update(self, scroll):
      self.rect.x += scroll

class StaticTile(Tile):
    def __init__(self, size, x, y, surface):
       super().__init__(size, x, y)
       self.image = surface