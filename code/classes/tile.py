import pygame 
from settings import *
from functions.support import * 

class Tile(pygame.sprite.Sprite):
    def __init__(self, size, x, y):
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
       
class Coin(AnimatedTile):
   def __init__(self, size, x, y, path):
      super().__init__(size, x, y, path)
      centerX = x + tileSize // 2
      centerY = y + tileSize // 2
      self.rect = self.image.get_rect(center = (centerX, centerY))

class Palm(AnimatedTile):
   def __init__(self, size, x, y, path, offset):
      super().__init__(size, x, y, path)
      offset_y = y - offset
      self.rect.topleft = (x, offset_y)
      
class Water:
  def __init__(self, top, levelWidth):
     waterStart = -screenWidth
     waterTileWidth = 192
     tile_x_amount = int((levelWidth + screenWidth * 2) / waterTileWidth)
     self.waterSprites = pygame.sprite.Group()

     for tile in range(tile_x_amount):
        x = tile * waterTileWidth + waterStart
        y = top
        sprite = AnimatedTile(waterTileWidth, x, y, './graphics/decoration/water')
        self.waterSprites.add(sprite)
        
  def draw(self, surface, scroll):
     self.waterSprites.update(scroll)
     self.waterSprites.draw(surface)
                              
