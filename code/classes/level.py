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
        self.currentX = 0

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
    
    def scroll_x(self):       
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x

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

    def horizontalCollision(self):
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed

        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0:
                    player.rect.left = sprite.rect.right
                    player.onLeft = True
                    self.currentX = player.rect.left
                elif player.direction.x > 0:
                    player.rect.right = sprite.rect.left
                    player.onRight = True
                    self.currentX = player.rect.right 
                    
        if player.onLeft and (player.rect.left < self.currentX or player.direction.x >= 0):
            player.onLeft = False
        if player.onLeft and (player.rect.right > self.currentX or player.direction.x <= 0):
            player.onRight = False
           
    def verticalCollision(self):
        player = self.player.sprite
        player.applyGravity()

        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0
                    player.onGround = True
                elif player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0
                    player.onCeiling = True

        if player.onGround and player.direction.y < 0 or player.direction.y > 1:
            player.onGround = False
        if player.onCeiling and player.direction.y > 0:
            player.onCeiling = False
            
    def draw(self):
        self.tiles.update(self.worldScroll)
        self.tiles.draw(self.displaySurface)
        self.scroll_x()
        
        #player
        self.player.update()
        self.horizontalCollision()
        self.verticalCollision()
        self.player.draw(self.displaySurface)
