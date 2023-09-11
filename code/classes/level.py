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
    def __init__(self, currentLevel, surface, createOverworld, updateCoins, changeHealth):
        self.displaySurface = surface
        self.worldScroll = 0
        self.bgScroll = bgScroll
        self.currentX = 0
        self.changehealth = changeHealth

        #overworld
        self.currentLevel = currentLevel
        self.createOverworld = createOverworld
        levelData = levels[self.currentLevel]
        self.new_max_level = levelData['unlock']
        
        
        playerLayout = import_csv_layout(levelData['player'])
        self.player = pygame.sprite.GroupSingle()
        self.goal = pygame.sprite.GroupSingle()
        self.cameraGroup = CameraGroup()

        #UI
        self.updateCoins = updateCoins

        self.explosionSprites = pygame.sprite.Group()

        #importing background leaves
        constraintLayout = import_csv_layout(levelData['constraint'])
        self.constraintSprites = self.create_tile_group(constraintLayout, 'constraint')

        leaveLayout = import_csv_layout(levelData['leaves'])
        self.leaveSprites = self.create_tile_group(leaveLayout, 'leaves')

        #importing terrain from CSV files
        terrainLayout = import_csv_layout(levelData['terrain'])
        self.terrainSprites = self.create_tile_group(terrainLayout, 'terrain')



        #foreground palms
        fg_palm_layout = import_csv_layout(levelData['fg palms'])
        self.fg_palm_sprites = self.create_tile_group(fg_palm_layout, 'fg palms')

        bg_palm_layout = import_csv_layout(levelData['bg palms'])
        self.bg_palm_sprites = self.create_tile_group(bg_palm_layout, 'bg palms')

        opossumLayout = import_csv_layout(levelData['opossum'])
        self.opossumSprites = self.create_tile_group(opossumLayout, 'opossum')

        #import coin
        coinsLayout = import_csv_layout(levelData['coins'])
        self.coinSprites = self.create_tile_group(coinsLayout, 'coins')

        self.playerSetup(playerLayout, changeHealth)
        levelWidth = len(terrainLayout[0])  * tileSize


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
                        sprite = StaticTile(tileSize, x, y, tileSurface, self.cameraGroup)

                    if type == 'leaves':
                        leaves_tile_list = import_cut_graphics('./graphics/terrain/jungle tileset.png')
                        tileSurface = leaves_tile_list[int(value)]
                        sprite = StaticTile(tileSize, x, y, tileSurface, self.cameraGroup)

                    if type == 'coins':
                        if value == '58': sprite = Coin(tileSize, x, y, './graphics/coins/gold', self.cameraGroup, 5)
                        if value == '116': sprite = Coin(tileSize, x, y, './graphics/coins/silver', self.cameraGroup, 1)

                    if type == 'fg palms':
                        if value == "0":
                            sprite = Palm(64, x, y, './graphics/terrain/palm_small', 85, self.cameraGroup)
                        if value == "1": 
                            sprite = Palm(64, x, y, './graphics/terrain/palm_large', 120, self.cameraGroup)

                    if type == 'bg palms':
                        sprite = Palm(tileSize, x, y, './graphics/terrain/palm_bg', 110, self.cameraGroup)

                    if type == 'opossum':
                        sprite = Opossum(tileSize, x, y, self.cameraGroup)

                    if type == 'constraint':
                        terrain_tile_list = import_cut_graphics('./graphics/terrain/jungle tileset.png')
                        tileSurface = terrain_tile_list[int(value)]
                        sprite = StaticTile(tileSize, x, y, tileSurface, self.cameraGroup)

                    spriteGroup.add(sprite)                       
        return spriteGroup

    def playerSetup(self, layout, changeHealth):
        for row_index, row in enumerate(layout):
            for column_index, value in enumerate(row):
                x = column_index * tileSize
                y = row_index * tileSize
                if value == '0':
                    sprite = Player((x,y), self.cameraGroup, changeHealth)
                    self.player.add(sprite)
                if value == '1':
                    hatSurface = pygame.image.load('./graphics/character/hat.png')
                    sprite = StaticTile(tileSize, x, y, hatSurface, self.cameraGroup)
                    self.goal.add(sprite)
    
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
                    player.releasedJump = False
                elif player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0
                    player.onCeiling = True
                    player.releasedJump = False

        if player.onGround and player.direction.y < 0 or player.direction.y > 1:
            player.onGround = False
        if player.onCeiling and player.direction.y > 0:
            player.onCeiling = False

    #part two

    def opossumCollision(self):
        for opossum in self.opossumSprites.sprites():
            if pygame.sprite.spritecollide(opossum, self.constraintSprites, False):
                opossum.reverse()

    def checkDeath(self):
        #if player off screen + camera offset
        if self.player.sprite.rect.top > screenHeight + 143:
            self.changehealth(-1)
            self.createOverworld(self.currentLevel, 0)
    
    def checkWin(self):
        if pygame.sprite.spritecollide(self.player.sprite, self.goal, False):
            self.changehealth(1)
            self.createOverworld(self.currentLevel, self.new_max_level)    

    def checkCoin(self):
        collidedCoins = pygame.sprite.spritecollide(self.player.sprite, self.coinSprites, True)
        if collidedCoins:
            for coin in collidedCoins:
                self.updateCoins(coin.value)

    def checkOpossumCollisions(self):
        opossumCollisions = pygame.sprite.spritecollide(self.player.sprite, self.opossumSprites, False)

        if opossumCollisions:
            for opossum in opossumCollisions:
                opossumCenter = opossum.rect.centery
                opossumTop = opossum.rect.top
                playerBottom = self.player.sprite.rect.bottom

                if opossumTop < playerBottom and self.player.sprite.direction.y > 0:
                    self.player.sprite.direction.y = -10
                    explosionSprite = ParticleEffect(opossum.rect.center, 'explosion', self.cameraGroup)
                    self.explosionSprites.add(explosionSprite)
                    opossum.kill()
                else:
                    if self.player.sprite.paused == False:
                        self.player.sprite.getDamage()

    def run(self):

        self.opossumCollision()

        self.cameraGroup.update()
        self.cameraGroup.customDraw(self.player)

        self.horizontalCollision()
        self.verticalCollision()

        self.checkDeath()
        self.checkWin()
        self.checkCoin()
        self.checkOpossumCollisions()


    