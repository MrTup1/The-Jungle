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
        self.healthAdded = False
        self.completedLevel = False

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
        self.resumeImg = pygame.image.load("./graphics/ui/Resume.png").convert_alpha() #Image for buttons
        self.optionsImg = pygame.image.load("./graphics/ui/Options.png").convert_alpha()
        self.quitImg = pygame.image.load("./graphics/ui/Quit.png").convert_alpha() 

        self.resumeButton = Button(400, 110, self.resumeImg, 1) #Create an actual button in pygame for each button
        self.optionsButton = Button(400, 220, self.optionsImg, 1)
        self.quitButton = Button(400, 330, self.quitImg, 1)

        self.explosionSprites = pygame.sprite.Group()

        #importing background leaves, each layer is in a CSV format, and are each imported below
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
        leaves_tile_list = import_cut_graphics('./graphics/terrain/jungle tileset.png') #Slice tileset into 16x16 pixels
        terrain_tile_list = import_cut_graphics('./graphics/terrain/jungle tileset.png') 
        
        for row_index, row in enumerate(layout): #Iterate over every row and column in CSV file 
            for column_index, value in enumerate(row):
                if value != '-1': #If tile is not empty
                    x = column_index * tileSize #Get coordinates of tile
                    y = row_index * tileSize

                    if type == 'terrain': #Check if the tile is in this specific layer
                        tileSurface = terrain_tile_list[int(value)] #Get corresponding graphic from sliced tileset
                        sprite = StaticTile(tileSize, x, y, tileSurface, self.cameraGroup) #Place a tile at this location

                    if type == 'leaves':  
                        tileSurface = leaves_tile_list[int(value)]
                        sprite = StaticTile(tileSize, x, y, tileSurface, self.cameraGroup)

                    if type == 'coins':
                        if value == '58': sprite = Coin(tileSize, x, y, './graphics/coins/gold', self.cameraGroup, 5)
                        if value == '116': sprite = Coin(tileSize, x, y, './graphics/coins/silver', self.cameraGroup, 1)

                    if type == 'fg palms':
                        if value == "0": #Corresponding ID for small palm trees in Tiled
                            sprite = Palm(64, x, y, './graphics/terrain/palm_small', 85, self.cameraGroup)
                        if value == "1": #Corresponding ID for big palm trees in Tiled
                            sprite = Palm(64, x, y, './graphics/terrain/palm_large', 120, self.cameraGroup)

                    if type == 'bg palms':
                        sprite = Palm(tileSize, x, y, './graphics/terrain/palm_bg', 110, self.cameraGroup)

                    if type == 'opossum':
                        sprite = Opossum(tileSize, x, y, self.cameraGroup)

                    if type == 'constraint':
                        tileSurface = terrain_tile_list[int(value)]
                        sprite = StaticTile(tileSize, x, y, tileSurface, self.cameraGroup)

                    spriteGroup.add(sprite) #Create a sprite group for each layer                       
        return spriteGroup

    def playerSetup(self, layout, changeHealth): 
        for row_index, row in enumerate(layout):
            for column_index, value in enumerate(row):
                x = column_index * tileSize #Origin x and y coordinates of player from Tiled 
                y = row_index * tileSize
                if value == '0': #Tiled ID is 0 for player sprite, so if 0 is present, it is the player
                    self.spawnX = x
                    self.spawnY = y
                    sprite = Player((x,y), self.cameraGroup, changeHealth, self.paused, self.currentLevel) #New parameter
                    self.player.add(sprite)
                if value == '1': #Tiled ID is 1 for destination sprite
                    hatSurface = pygame.image.load('./graphics/character/hat.png')
                    sprite = StaticTile(28, x, y, hatSurface, self.cameraGroup) #Place destination sprite 
                    self.goal.add(sprite)
    
    def horizontalCollision(self):
        player = self.player.sprite
        player.collisionRect.x += player.direction.x * player.speed #Move collision rectangle
        collidableSprites = self.terrainSprites.sprites() + self.fg_palm_sprites.sprites() #Only terrain and palm trees are collidable

        for sprite in collidableSprites: 
            if sprite.rect.colliderect(player.collisionRect): #Check if there is a collision between player and one of the sprites in collidable sprites
                if player.direction.x < 0: #If player is moving left
                    player.collisionRect.left = sprite.rect.right #Prevent player moving further, set equal coordinates for their rectangle's edges
                    player.onLeft = True
                    self.currentX = player.collisionRect.left
                elif player.direction.x > 0: #If player is moving right
                    player.collisionRect.right = sprite.rect.left
                    player.onRight = True
                    self.currentX = player.collisionRect.right 
                    

    def verticalCollision(self):
        player = self.player.sprite
        if self.paused == False and self.out_of_screen == False: #Apply gravity at all times except game paused or player out of screen
            player.applyGravity()
        collidableSprites = self.terrainSprites.sprites() + self.fg_palm_sprites.sprites() #Only terrain and palm trees are collidable

        for sprite in collidableSprites:
            if sprite.rect.colliderect(player.collisionRect):
                if player.direction.y > 0: #If player is moving downwards 
                    player.collisionRect.bottom = sprite.rect.top #Prevent player moving further downwards
                    player.direction.y = 0 #Reduce gravity to 0 
                    player.onGround = True
                    if player.firstOnGround: #Get time when player first on ground
                        player.onGroundTime = time.time()
                        player.firstOnGround = False
                    player.releasedJump = False
                elif player.direction.y < 0: #If player is moving upwards
                    player.collisionRect.top = sprite.rect.bottom #Prevent player moving further upwards
                    player.direction.y = 0 #Reduce gravity to 0
                    player.onCeiling = True 
                    player.releasedJump = False

        if player.onGround and player.direction.y < 0 or player.direction.y > 1:
            #Reset all player attributes
            player.onGround = False
            player.firstOnGround = True 
            player.opossumVulnerability = False

        if player.onCeiling and player.direction.y > 0:
            player.onCeiling = False           

    def opossumCollision(self): #Detect when opossum hits a constraint sprite, which reverses its direction
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
        if pygame.sprite.spritecollide(self.player.sprite, self.goal, False): #Check if player reached destination
            self.completedLevel = True
            keys = pygame.key.get_pressed()
            if not self.healthAdded: #If this is the first time player collided with destination sprite 
                self.changehealth(1)
                self.healthAdded = True
            if self.new_max_level == 2: #Check if level is the level that unlocks Dash
                self.ui.drawBlackOverlay()
                self.ui.unlockdashAbility() #display the UI when unlocking the dash ability
                if keys[pygame.K_SPACE] or keys[pygame.K_RETURN]: #Check when player presses space, so they return to the overworld
                    self.createOverworld(self.currentLevel, self.new_max_level)    
            elif self.new_max_level == 3: #Check if level is the level that unlcoks Double Jump  
                self.ui.drawBlackOverlay()
                self.ui.unlockDoubleAbility() #display the UI when unlocking the double jump ability
                if keys[pygame.K_SPACE] or keys[pygame.K_RETURN]:
                    self.createOverworld(self.currentLevel, self.new_max_level)       
            else:
                self.createOverworld(self.currentLevel, self.new_max_level)    

    def checkCoin(self): #Check collision between player and coin
        collidedCoins = pygame.sprite.spritecollide(self.player.sprite, self.coinSprites, True)
        if collidedCoins:
            for coin in collidedCoins:
                self.updateCoins(coin.value) #Update coin UI based on the collided coin's value (1 or 5)

    def checkOpossumCollisions(self): #Check opossum collision with player
        player = self.player.sprite
        opossumCollisions = pygame.sprite.spritecollide(player, self.opossumSprites, False) 

        if opossumCollisions: #When player has collided with an opossum
            for opossum in opossumCollisions:
                collisionTime = time.time()
                if collisionTime - player.onGroundTime >= 0.01: #Check opossum on time longer than 30ms
                    player.opossumVulnerability = True #Opossum can kill player when sent to true

                opossumTop = opossum.rect.top
                playerBottom = player.collisionRect.bottom

                #First if statement checks if player has killed opossum    
                if (opossumTop < playerBottom and player.direction.y) > 0 or (opossumTop < playerBottom and player.opossumVulnerability == False): #Alt condition, so player can kill opossum 30ms before taking damage
                    player.direction.y = -10 #Moves player upwards, allowing time to react
                    explosionSprite = ParticleEffect(opossum.rect.center, 'explosion', self.cameraGroup) #Draw particle effect at location opossum died
                    self.explosionSprites.add(explosionSprite) 
                    opossum.kill() #Remove opossum from game
                else:
                    if player.paused == False: 
                        player.getDamage()

    def menu(self): #Pause menu UI
        if self.paused: 
            self.ui.drawBlackOverlay() 
            if self.resumeButton.draw(screen): #If resume button pressed
                self.paused = False
            if self.optionsButton.draw(screen): #If options button pressed
                print("Options")
            if self.quitButton.draw(screen): #If quit button pressed
                self.createOverworld(self.currentLevel, 0) #Return to overworld

    def checkPause(self): 
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]: 
            if self.paused == True: #Paused State (When player presses pause when in pause menu)
                self.time2 = time.time()
                if (self.time2 - self.time1 >= self.pausedCooldown): #Prevent pause spamming by adding cooldown
                    self.time2 = time.time()
                    #Load paused velocity in x and y direction
                    self.player.sprite.direction.x = self.player.sprite.pausedDirectionX 
                    self.player.sprite.direction.y = self.player.sprite.pausedDirectionY
                    self.paused = False
            else:	#Game State (When player presses pause when playing game)
                self.time1 = time.time()
                if (self.time1 - self.time2 >= self.pausedCooldown):
                    #Save saved paused velocities when game is paused
                    self.player.sprite.pausedDirectionX = self.player.sprite.direction.x
                    self.player.sprite.pausedDirectionY = self.player.sprite.direction.y

                    #Prevent player from moving while paused
                    self.player.sprite.direction.y = 0 
                    self.player.sprite.direction.x = 0
                    self.paused = True

    def run(self): #Update function for the level class
        if self.paused == False and self.dead == False and not self.completedLevel: #Player must both be alive and not paused for game to run
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


    