import pygame
import time
from game_data import levels
from functions.support import * 
from classes.tile import AnimatedTile
from functions.background import OverworldBackground

class Node(pygame.sprite.Sprite): #Class stores all attributes and methods of a singular node(level icon) in the overworld
    def __init__(self, pos, status, iconSpeed, path):
        super().__init__()
        self.frames = importFolder(path)
        self.frameIndex = 0
        self.animationSpeed = 0.15
        self.image = pygame.transform.scale_by(self.frames[self.frameIndex], 0.5) #Scale each image from animation down by a scale factor of 2
        if status == 'available': #If level is locked or not
            self.status = 'available'
        else:
            self.status = 'locked'

        self.rect = self.image.get_rect(center = pos)
        self.hitbox = pygame.Rect(self.rect.centerx - iconSpeed / 2, self.rect.centery - iconSpeed / 2, iconSpeed, iconSpeed) #Define boundaries of player sprite hitbox

    def animate(self): #Logic for animating each node icon (same as player animation)
        self.frameIndex += self.animationSpeed
        if (self.frameIndex >= len(self.frames)):
          self.frameIndex = 0
        self.image = pygame.transform.scale_by(self.frames[int(self.frameIndex)], 0.5)

    def update(self): #Function called 60 times a second
        if self.status == 'available': #Animate icon
            self.animate()
        else: #If node icon locked, produce the same image fully opaque in black
            blackSurf = self.image.copy() 
            blackSurf.fill('black', None, pygame.BLEND_RGBA_MULT)
            self.image.blit(blackSurf, (0,0))

class Icon(pygame.sprite.Sprite): #Player icon class
    def __init__(self, pos):
        super().__init__()
        self.pos = pos
        self.image = pygame.transform.scale_by(pygame.image.load('./graphics/overworld/hat.png'), 0.75).convert_alpha()
        self.rect = self.image.get_rect(center = pos)
    
    def update(self):
        self.rect.center = self.pos #Update position of icon when moving

class Overworld: #Main class of level selection screen)
    def __init__(self, startLevel, maxLevel, surface, createLevel, createStart):
        self.displaySurface = surface
        self.maxLevel = maxLevel
        self.currentLevel = startLevel
        self.moving = False
        self.createLevel = createLevel #Get function from game class to create level
        self.createStart = createStart #Get function from game class to create start screen

        self.moveDirection = pygame.math.Vector2(0,0) #Vector storing direction of player icon
        self.speed = 8

        self.background = pygame.image.load('./graphics/overworld/plank_background.png').convert_alpha()

        self.setupNodes()
        self.setupIcon()

        self.createTime = time.time()
        self.createWait = 0.25

    def setupNodes(self): #Place nodes in location from specified in dictionary
        self.nodes = pygame.sprite.Group()

        for index, nodeData in enumerate(levels.values()): #Iterate over each key (each level), and obtain their corresponding node location
            if index <= self.maxLevel: #Check if player has unlocked level yet             
              nodeSprite = Node(nodeData['nodePos'], 'available', self.speed, nodeData['nodeGraphic'])
            else:  #If player has not unlocked this level
              nodeSprite = Node(nodeData['nodePos'], 'locked', self.speed, nodeData['nodeGraphic'])
            self.nodes.add(nodeSprite)

    def setupIcon(self): #Place player icon sprite 
        self.icon = pygame.sprite.GroupSingle()
        iconSprite = Icon(self.nodes.sprites()[self.currentLevel].rect.center)
        self.icon.add(iconSprite)

    def drawPaths(self): #Draw lines between each level node
        if self.maxLevel > 0:
            pointList = []
            for index, nodeData in enumerate(levels.values()): #Creates a list of points for all the level nodes
                if index <= self.maxLevel:             
                    pointList.append(nodeData['nodePos']) 
            pygame.draw.lines(self.displaySurface, '#582c35', False, pointList, 6) #Draws lines between adjacent points in the list

    def input(self): #Obtain input from player
        keys = pygame.key.get_pressed()
        currentTime = time.time()
        if not self.moving and currentTime - self.createTime >= self.createWait: #added delay before input
            if keys[pygame.K_RIGHT] and self.currentLevel < self.maxLevel: #Move player to the right by one node after pressing right arrow
                self.moveDirection = self.getMovementData(True)
                self.currentLevel += 1
                self.moving = True
            elif keys[pygame.K_LEFT] and self.currentLevel > 0: #Move player to the left by one level node after pressing left arrow
                self.moveDirection = self.getMovementData(False)
                self.currentLevel -= 1
                self.moving = True
            elif keys[pygame.K_SPACE] or keys[pygame.K_RETURN]: #Select level to play
                self.createLevel(self.currentLevel)
            elif keys[pygame.K_ESCAPE]: #Return to start screen
                self.createStart(self.currentLevel)
    
    def updateIconPosition(self): #Move player icon sprite
        if self.moving and self.moveDirection:
            self.icon.sprite.pos += self.moveDirection * self.speed
            targetNode = self.nodes.sprites()[self.currentLevel]

            if targetNode.hitbox.collidepoint(self.icon.sprite.pos):
                self.moving = False
                self.moveDirection= pygame.math.Vector2(0,0) 

    def getMovementData(self, direction): #Create vector of direction where player should be moving to 
        start = pygame.math.Vector2(self.nodes.sprites()[self.currentLevel].rect.center)
        if direction: #Check if player is moving right (top) or moving left (bottom)
            end = pygame.math.Vector2(self.nodes.sprites()[self.currentLevel + 1].rect.center)
        else:
            end = pygame.math.Vector2(self.nodes.sprites()[self.currentLevel - 1].rect.center)

        final = (end - start).normalize() #Get unit vector pointing start node to end node
        return (final)
    
    def getMaxLevel(self):
        return self.maxLevel
    
    def run(self): #Functions to update continously 
        self.input()
        self.updateIconPosition()
        self.icon.update()

        self.displaySurface.blit(self.background, (0,0))
        self.drawPaths()
        self.nodes.draw(self.displaySurface)
        self.nodes.update()
        self.icon.draw(self.displaySurface)

