from os import walk
from csv import reader
import pygame
from settings import *

def importFolder(path):
    surfaceList = []
    
    for _,__,imgFiles in walk(path):
      for image in imgFiles:
          fullPath = path + '/' + image
          imageSurf = pygame.image.load(fullPath).convert_alpha()
          surfaceList.append(imageSurf) 

    return surfaceList

def import_csv_layout(path):
   terrainMap = []
   with open(path) as map:
      level = reader(map, delimiter= ',')
      for row in level:
         terrainMap.append(list(row))
   return terrainMap

def import_cut_graphics(path):
   surface = pygame.image.load(path).convert_alpha()
   tile_num_x = int(surface.get_width() // tileSize)
   tile_num_y = int(surface.get_height() // tileSize)

   cutTiles = []
   for row in range(tile_num_y):
      for column in range(tile_num_x):
         x = column * tileSize
         y = row * tileSize
         newSurface = pygame.Surface((tileSize, tileSize), flags = pygame.SRCALPHA)
         newSurface.blit(surface, (0,0), (x,y,tileSize,tileSize))
         cutTiles.append(newSurface)

   return cutTiles

class ParticleEffect(pygame.sprite.Sprite):
   def __init__(self, pos, type, group):
      super().__init__(group)
      self.frameIndex = 0
      self.animationSpeed = 0.5
      if type == 'explosion':
         self.frames = importFolder('./graphics/enemy/explosion')
      self.image = self.frames[self.frameIndex]
      self.rect = self.image.get_rect(center = pos)
   
   def animate(self):
      self.frameIndex += self.animationSpeed
      if self.frameIndex >= len(self.frames):
         self.kill()
      else:
         self.image = self.frames[int(self.frameIndex)]
   
   def update(self):
      self.animate()

