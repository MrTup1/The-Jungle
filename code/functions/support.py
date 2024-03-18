from os import walk
from csv import reader
import pygame
from settings import *

def importFolder(path):#Imports images in a directory into one array as a pygame surface
    surfaceList = []
    
    for _,__,imgFiles in walk(path): #Loop overy each image in a file path
      for image in imgFiles:
          fullPath = path + '/' + image
          imageSurf = pygame.image.load(fullPath).convert_alpha()
          surfaceList.append(imageSurf) 

    return surfaceList #Return array of surfaces which can be drawn onto a screen

def import_csv_layout(path): #Convert CSV file format into a 2 dimensional array
   terrainMap = []
   with open(path) as map: #Open CSV file 
      level = reader(map, delimiter= ',')
      for row in level: 
         terrainMap.append(list(row)) #Each index represents one row (stored as a list) in the CSV file 
   return terrainMap

def import_cut_graphics(path): #Slice tileset into 16x16 squares
   surface = pygame.image.load(path).convert_alpha()
   tile_num_x = int(surface.get_width() // tileSize) #Obtain total tile number in horizontal direction
   tile_num_y = int(surface.get_height() // tileSize) #Obtain total tile number in verticals direction

   cutTiles = []
   for row in range(tile_num_y): #Iterate every row
      for column in range(tile_num_x): #Iterate every column
         x = column * tileSize #Get x coordinate sof tile
         y = row * tileSize #Get y coordinate of tile
         newSurface = pygame.Surface((tileSize, tileSize), flags = pygame.SRCALPHA) 
         newSurface.blit(surface, (0,0), (x,y,tileSize,tileSize)) #Crop original tileset image into a 16x16 tile surface
         cutTiles.append(newSurface) #Add 16x16 surface to surface list

   return cutTiles

class ParticleEffect(pygame.sprite.Sprite): #Displays a particle effect
   def __init__(self, pos, type, group):
      super().__init__(group)
      self.frameIndex = 0
      self.animationSpeed = 0.5
      if type == 'explosion':
         self.frames = importFolder('./graphics/enemy/explosion')
      self.image = self.frames[self.frameIndex]
      self.rect = self.image.get_rect(center = pos) #Draws particle effect at a specified position in parameters
   
   def animate(self):
      self.frameIndex += self.animationSpeed
      if self.frameIndex >= len(self.frames):
         self.kill() #If all images are drawn, remove this particle effect
      else:
         self.image = self.frames[int(self.frameIndex)] #Draw particle effect if not all images are drawn yet
   
   def update(self): #Update function for particle effect class
      self.animate()

