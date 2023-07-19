import pygame
import time
from settings import *
from classes.tile import Tile
from classes.player import Player

class Level:
    def __init__(self, levelData, surface):
        self.displaySurface = surface
        self.Map = levelData
        self.worldScroll = 0

    def setupLevel(self):
        self.tiles = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()
        
        for row_index, row in enumerate(self.Map):
            for column_index, column in enumerate(row):
                x = column_index * tileSize
                y = row_index * tileSize

                if (column == "P"):
                    player_sprite = Player((x,y))
                    self.player.add(player_sprite)
                if (column == "X"):
                    tile = Tile(x, y, tileSize)
                    self.tiles.add(tile)
        print(self.tiles)
    
    def scroll_x(self):
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x

        print(direction_x)


        if player_x <= SCROLL_THRESH and direction_x == -1:
            self.worldScroll = 8
            player.speed = 0

        elif player_x >= screenWidth - SCROLL_THRESH and direction_x == 1:
            self.worldScroll = -8
            player.speed = 0
        else:
            self.worldScroll = 0
            player.speed = 8

        return (self.worldScroll)

    def draw(self):
        self.tiles.update(self.worldScroll)
        self.tiles.draw(self.displaySurface)
        
        #player
        self.player.update()
        self.player.draw(self.displaySurface)
        self.scroll_x()