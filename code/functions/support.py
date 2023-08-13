from os import walk
from csv import reader
import pygame

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

