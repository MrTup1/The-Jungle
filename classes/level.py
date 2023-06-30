import pygame
import time
from settings import *
from classes.tile import Tile

class Level:
    def __init__(self, levelData, surface):
        self.displaySurface = surface
        self.Map = levelData

    def setupLevel(self):
        self.tiles = pygame.sprite.Group()
        for row_index, row in enumerate(self.Map):
            for column_index, column in enumerate(row):
                if (column == "P"):
                    x = column_index * tileSize
                    y = row_index * tileSize 
                if (column == "X"):
                    x = column_index * tileSize
                    y = row_index * tileSize
                    tile = Tile(x, y, tileSize)
                    self.tiles.add(tile)
        print(self.tiles)
   
    def draw(self , scroll):
        self.tiles.update(scroll)
        self.tiles.draw(self.displaySurface)