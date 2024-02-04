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
from functions.button import Button
from classes.ui import UI
import numpy as np

class Level:
    def __init__(self, currentLevel, surface, createOverworld, updateCoins, changeHealth):
        self.displaySurface = surface
        self.worldScroll = 0
        self.bgScroll = bgScroll
        self.currentX = 0
        self.changehealth = changeHealth
        
        #Pause
        self.pauseDirection = 0
        self.pausedCooldown = 0.25
        self.paused = False
        self.time1 = 0
        self.time2 = 0 

        #overworld
        self.currentLevel = currentLevel
        self.createOverworld = createOverworld
        levelData = levels[self.currentLevel]
        self.new_max_level = levelData['unlock']
        
        #Death
        self.out_of_screen = False
        self.dead = False
        self.spawnX = 10
        self.spawnY = 10
        
        self.ui = UI(screen)

        playerLayout = import_csv_layout(levelData['player'])
        self.player = pygame.sprite.GroupSingle()
        self.goal = pygame.sprite.GroupSingle()
        self.cameraGroup = CameraGroup()

        #UI
        self.updateCoins = updateCoins
        self.resumeImg = pygame.image.load("./graphics/ui/Resume.png").convert_alpha()
        self.optionsImg = pygame.image.load("./graphics/ui/Options.png").convert_alpha()
        self.quitImg = pygame.image.load("./graphics/ui/Quit.png").convert_alpha() 

        self.resumeButton = Button(400, 110, self.resumeImg, 1)
        self.optionsButton = Button(400, 220, self.optionsImg, 1)
        self.quitButton = Button(400, 330, self.quitImg, 1)

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
        leaves_tile_list = import_cut_graphics('./graphics/terrain/jungle tileset.png')
        terrain_tile_list = import_cut_graphics('./graphics/terrain/jungle tileset.png')
        
        for row_index, row in enumerate(layout):
            for column_index, value in enumerate(row):
                if value != '-1':
                    x = column_index * tileSize
                    y = row_index * tileSize

                    if type == 'terrain': 
                        tileSurface = terrain_tile_list[int(value)]
                        sprite = StaticTile(tileSize, x, y, tileSurface, self.cameraGroup)

                    if type == 'leaves':
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
                    self.spawnX = x
                    self.spawnY = y
                    sprite = Player((x,y), self.cameraGroup, changeHealth, self.paused, self.currentLevel)
                    self.player.add(sprite)
                if value == '1':
                    hatSurface = pygame.image.load('./graphics/character/hat.png')
                    sprite = StaticTile(28, x, y, hatSurface, self.cameraGroup)
                    self.goal.add(sprite)
    
    def horizontalCollision(self):
        player = self.player.sprite
        player.collisionRect.x += player.direction.x * player.speed
        collidableSprites = self.terrainSprites.sprites() + self.fg_palm_sprites.sprites()

        for sprite in collidableSprites:
            if sprite.rect.colliderect(player.collisionRect):
                if player.direction.x < 0:
                    player.collisionRect.left = sprite.rect.right
                    player.onLeft = True
                    self.currentX = player.collisionRect.left
                elif player.direction.x > 0:
                    player.collisionRect.right = sprite.rect.left
                    player.onRight = True
                    self.currentX = player.collisionRect.right 
                    

    def verticalCollision(self):
        player = self.player.sprite
        if self.paused == False and self.out_of_screen == False:
            player.applyGravity()
        collidableSprites = self.terrainSprites.sprites() + self.fg_palm_sprites.sprites()

        for sprite in collidableSprites:
            if sprite.rect.colliderect(player.collisionRect):
                if player.direction.y > 0:
                    player.collisionRect.bottom = sprite.rect.top
                    player.direction.y = 0
                    player.onGround = True
                    player.releasedJump = False
                elif player.direction.y < 0:
                    player.collisionRect.top = sprite.rect.bottom
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
        if self.player.sprite.rect.top > screenHeight + 143 and self.out_of_screen == False:
            self.out_of_screen = True #Prevent continously damaging player
            self.player.sprite.collisionRect.topleft = (self.spawnX, self.spawnY) #Teleport to where player spawned
            #New added
            self.player.sprite.createTime = time.time() #Reset spawn time
            self.player.sprite.direction.x = 0 #Prevent movement immediately after spawning
            self.player.sprite.direction.y = 0
            
            self.player.sprite.getDamage() #Decrease by one health and invincible
            self.out_of_screen = False #End of damage sequence
    
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

    def menu(self):
        if self.paused: 
            self.ui.drawBlackOverlay() 
            if self.resumeButton.draw(screen):
                self.paused = False
            if self.optionsButton.draw(screen):
                print("Options")
            if self.quitButton.draw(screen):
                self.createOverworld(self.currentLevel, 0)

    def checkPause(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            if self.paused == True: #Paused State
                self.time2 = time.time()
                if (self.time2 - self.time1 >= self.pausedCooldown):
                    self.time2 = time.time()
                    self.player.sprite.direction.x = self.player.sprite.pausedDirectionX
                    self.player.sprite.direction.y = self.player.sprite.pausedDirectionY
                    self.paused = False
            else:	#Game State
                self.time1 = time.time()
                if (self.time1 - self.time2 >= self.pausedCooldown):
                    self.player.sprite.pausedDirectionX = self.player.sprite.direction.x
                    self.player.sprite.pausedDirectionY = self.player.sprite.direction.y
                    self.player.sprite.direction.y = 0
                    self.player.sprite.direction.x = 0
                    self.paused = True

    def run(self):
        if self.paused == False and self.dead == False: #Player must both be alive and not paused for game to run
            self.cameraGroup.update() #Method for updating all tiles and enemies

        self.checkPause()
        self.opossumCollision()
        self.cameraGroup.customDraw(self.player)


        self.horizontalCollision()
        self.verticalCollision()

        self.checkDeath()
        self.checkWin()
        self.checkCoin()
        self.checkOpossumCollisions()
        self.menu()


    