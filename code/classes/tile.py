import pygame 
from settings import *
from functions.support import *

class Tile(pygame.sprite.Sprite):
    def __init__(self, x, y, size):
      super().__init__()
      self.image = pygame.Surface((size, size))
      self.image.fill('GREEN')
      self.rect = self.image.get_rect()
      self.rect.x = x
      self.rect.y = y
    
    def update(self, scroll):
      self.rect.x += scroll

class StaticTile(Tile):
    def __init__(self, size, x, y, surface):
       super().__init__(size, x, y)
       self.image = surface

class AnimatedTile(Tile):
    def __init__(self, size, x, y, path):
       super().__init__(size, x, y)
       self.frames = importFolder(path)
       self.frameIndex = 0
       self.animationSpeed = 0.15
       self.image = self.frames[self.frameIndex]

    def animate(self):
       self.frameIndex += self.animationSpeed
       if (self.frameIndex >= len(self.frames)):
          self.frameIndex = 0
       self.image = self.frames[int(self.frameIndex)]
    
    def update(self,scroll):
       self.rect.x += scroll
       self.animate()
       


                              
