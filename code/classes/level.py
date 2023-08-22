import pygame
import time
from settings import *
from game_data import *
from classes.tile import Tile, StaticTile, AnimatedTile, Coin, Palm, Water
from classes.player import Player
from functions.support import *
from classes.opossum import Opossum
from classes.camera import CameraGroup
from functions.background import Background

class Level:
    def __init__(self, levelData, surface):
        self.displaySurface = surface
        self.Map = levelData
        self.worldScroll = 0
        self.bgScroll = bgScroll
        self.currentX = 0
        
        playerLayout = import_csv_layout(levelData['player'])
        self.player = pygame.sprite.GroupSingle()
        self.goal = pygame.sprite.GroupSingle()
        self.cameraGroup = CameraGroup()
        self.playerSetup(playerLayout)

        #importing background leaves
        leaveLayout = import_csv_layout(levelData['leaves'])
        self.leaveSprites = self.create_tile_group(leaveLayout, 'leaves')

        #importing terrain from CSV files
        terrainLayout = import_csv_layout(levelData['terrain'])
        self.terrainSprites = self.create_tile_group(terrainLayout, 'terrain')

        #import coin
        coinsLayout = import_csv_layout(levelData['coins'])
        self.coinSprites = self.create_tile_group(coinsLayout, 'coins')

        #foreground palms
        fg_palm_layout = import_csv_layout(levelData['fg palms'])
        self.fg_palm_sprites = self.create_tile_group(fg_palm_layout, 'fg palms')

        bg_palm_layout = import_csv_layout(levelData['bg palms'])
        self.bg_palm_sprites = self.create_tile_group(bg_palm_layout, 'bg palms')

        opossumLayout = import_csv_layout(levelData['opossum'])
        self.opossumSprites = self.create_tile_group(opossumLayout, 'opossum')

        constraintLayout = import_csv_layout(levelData['constraint'])
        self.constraintSprites = self.create_tile_group(constraintLayout, 'constraint')


        self.background = Background()
        levelWidth = len(terrainLayout[0])  * tileSize
        self.water = Water(screenHeight - 25, levelWidth)


    def create_tile_group(self, layout, type):
        spriteGroup = pygame.sprite.Group()
        
        for row_index, row in enumerate(layout):
            for column_index, value in enumerate(row):
                if value != '-1':
                    x = column_index * tileSize
                    y = row_index * tileSize

                    if type == 'terrain': 
                        terrain_tile_list = import_cut_graphics('./graphics/terrain/jungle tileset.png')
                        tileSurface = terrain_tile_list[int(value)]
                        sprite = StaticTile(tileSize, x, y, tileSurface)

                    if type == 'leaves':
                        leaves_tile_list = import_cut_graphics('./graphics/terrain/jungle tileset.png')
                        tileSurface = leaves_tile_list[int(value)]
                        sprite = StaticTile(tileSize, x, y, tileSurface)

                    if type == 'coins':
                        if value == '58': sprite = Coin(tileSize, x, y, './graphics/coins/gold')
                        if value == '116': sprite = Coin(tileSize, x, y, './graphics/coins/silver')

                    if type == 'fg palms':
                        if value == "0":
                            sprite = Palm(64, x, y, './graphics/terrain/palm_small', 85)
                        if value == "1": 
                            sprite = Palm(64, x, y, './graphics/terrain/palm_large', 120)

                    if type == 'bg palms':
                        sprite = Palm(tileSize, x, y, './graphics/terrain/palm_bg', 110)

                    if type == 'opossum':
                        sprite = Opossum(tileSize, x, y)

                    if type == 'constraint':
                        sprite = Tile(tileSize, x, y)

                    spriteGroup.add(sprite)                       
        return spriteGroup

    def playerSetup(self, layout):
        for row_index, row in enumerate(layout):
            for column_index, value in enumerate(row):
                x = column_index * tileSize
                y = row_index * tileSize
                if value == '0':
                    sprite = Player((x,y))
                    self.player.add(sprite)
                if value == '1':
                    hatSurface = pygame.image.load('./graphics/character/hat.png')
                    sprite = StaticTile(tileSize, x, y, hatSurface)
                    self.goal.add(sprite)
    
    def scroll_x(self):       
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x

        if player_x <= SCROLL_THRESH and direction_x == -1:
            self.worldScroll = 4
            player.speed = 0

        elif player_x >= screenWidth - SCROLL_THRESH and direction_x == 1:
            self.worldScroll = -4
            player.speed = 0
        else:
            self.worldScroll = 0
            player.speed = 4

        return (self.worldScroll)

    def horizontalCollision(self):
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed
        collidableSprites = self.terrainSprites.sprites() + self.fg_palm_sprites.sprites()

        for sprite in collidableSprites:
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
        collidableSprites = self.terrainSprites.sprites() + self.fg_palm_sprites.sprites()

        for sprite in collidableSprites:
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

    #part two

    def opossumCollision(self):
        for opossum in self.opossumSprites.sprites():
            if pygame.sprite.spritecollide(opossum, self.constraintSprites, False):
                opossum.reverse()

    def getWorldScroll(self):
        self.bgScroll += self.worldScroll 

        return self.bgScroll

    def getCamera(self):
        return self.cameraGroup
    
    def run(self):
        self.background.draw(self.displaySurface, self.getWorldScroll())

        self.bg_palm_sprites.update(self.worldScroll)
        self.bg_palm_sprites.draw(self.displaySurface)

        self.leaveSprites.update(self.worldScroll)
        self.leaveSprites.draw(self.displaySurface)

        self.water.draw(self.displaySurface, self.worldScroll)

        self.terrainSprites.update(self.worldScroll)
        self.terrainSprites.draw(self.displaySurface)
        
        self.fg_palm_sprites.update(self.worldScroll)
        self.fg_palm_sprites.draw(self.displaySurface)

        self.opossumSprites.update(self.worldScroll)
        self.opossumCollision()
        self.constraintSprites.update(self.worldScroll)
        self.opossumSprites.draw(self.displaySurface)

        self.coinSprites.update(self.worldScroll)
        self.coinSprites.draw(self.displaySurface)
        
        self.player.update()
        self.player.draw(self.displaySurface)

        self.horizontalCollision()
        self.verticalCollision()
        self.scroll_x()
        self.goal.update(self.worldScroll)
        self.goal.draw(self.displaySurface)












    