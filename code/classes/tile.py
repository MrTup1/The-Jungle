import pygame 
from settings import *
from functions.support import * 

class Tile(pygame.sprite.Sprite): #Tile class refres to the individual 16x16 sized squares the level editor places
    def __init__(self, size, x, y, group):
      super().__init__(group)
      self.image = pygame.Surface((size, size)) 
      self.image.fill('GREEN')
      self.rect = self.image.get_rect()
      self.rect.x = x
      self.rect.y = y
    
    def update(self):
       pass

class StaticTile(Tile): #Static tile inherits from Tile class (Tiles with no animation)
    def __init__(self, size, x, y, surface, group):
       super().__init__(size, x, y, group)
       self.image = surface

class AnimatedTile(Tile): #Animated tile also inherits from Tile class
    def __init__(self, size, x, y, path, group):
       super().__init__(size, x, y, group) 
       self.frames = importFolder(path) #Get array of images for animated tile
       self.frameIndex = 0
       self.animationSpeed = 0.15
       self.image = self.frames[self.frameIndex]

    def animate(self): #Animation logic same as player
       self.frameIndex += self.animationSpeed
       if (self.frameIndex >= len(self.frames)):
          self.frameIndex = 0
       self.image = self.frames[int(self.frameIndex)]
    
    def update(self):
       self.animate()
       
class Coin(AnimatedTile): #Coin inherits from animated tile class
   def __init__(self, size, x, y, path, group, value):
      super().__init__(size, x, y, path, group)
      centerX = x + tileSize // 2 #Center needs to be offset, as by default, it is in the top left
      centerY = y + tileSize // 2
      self.rect = self.image.get_rect(center = (centerX, centerY))
      self.value = value #Value of specific coin passed in as parameter (1 for silver, 5 for gold)

class Palm(AnimatedTile): #Palm class (tress) inherits from animated tile class
   def __init__(self, size, x, y, path, offset, group):
      super().__init__(size, x, y, path, group)
      offset_y = y - offset #Palm trees are also not displayed correctly, so an offset is needed 
      self.rect.topleft = (x, offset_y)
                              
