import pygame
from game_data import levels
from functions.support import * 
from classes.tile import AnimatedTile
from functions.background import OverworldBackground

class Node(pygame.sprite.Sprite):
    def __init__(self, pos, status, iconSpeed, path):
        super().__init__()
        self.frames = importFolder(path)
        self.frameIndex = 0
        self.animationSpeed = 0.15
        self.image = pygame.transform.scale_by(self.frames[self.frameIndex], 0.5)
        if status == 'available':
            self.status = 'available'
        else:
            self.status = 'locked'

        self.rect = self.image.get_rect(center = pos)
        self.hitbox = pygame.Rect(self.rect.centerx - iconSpeed / 2, self.rect.centery - iconSpeed / 2, iconSpeed, iconSpeed)

    def animate(self):
        self.frameIndex += self.animationSpeed
        if (self.frameIndex >= len(self.frames)):
          self.frameIndex = 0
        self.image = pygame.transform.scale_by(self.frames[int(self.frameIndex)], 0.5)

    def update(self):
        if self.status == 'available':
            self.animate()
        else:
            blackSurf = self.image.copy()
            blackSurf.fill('black', None, pygame.BLEND_RGBA_MULT)
            self.image.blit(blackSurf, (0,0))

class Icon(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.pos = pos
        self.image = pygame.transform.scale_by(pygame.image.load('./graphics/overworld/hat.png'), 0.75).convert_alpha()
        self.rect = self.image.get_rect(center = pos)
    
    def update(self):
        self.rect.center = self.pos

class Overworld:
    def __init__(self, startLevel, maxLevel, surface, createLevel):
        self.displaySurface = surface
        self.maxLevel = maxLevel
        self.currentLevel = startLevel
        self.moving = False
        self.createLevel = createLevel

        self.moveDirection = pygame.math.Vector2(0,0)
        self.speed = 8

        self.background = OverworldBackground()

        self.setupNodes()
        self.setupIcon()

    def setupNodes(self):
        self.nodes = pygame.sprite.Group()

        for index, nodeData in enumerate(levels.values()):
            if index <= self.maxLevel:             
              nodeSprite = Node(nodeData['nodePos'], 'available', self.speed, nodeData['nodeGraphic'])
            else: 
              nodeSprite = Node(nodeData['nodePos'], 'locked', self.speed, nodeData['nodeGraphic'])
            self.nodes.add(nodeSprite)

    def setupIcon(self):
        self.icon = pygame.sprite.GroupSingle()
        iconSprite = Icon(self.nodes.sprites()[self.currentLevel].rect.center)
        self.icon.add(iconSprite)

    def drawPaths(self):
        pointList = []
        for index, nodeData in enumerate(levels.values()):
            if index <= self.maxLevel:             
                pointList.append(nodeData['nodePos'])
        pygame.draw.lines(self.displaySurface, '#af7765', False, pointList, 6)

    def input(self):
        keys = pygame.key.get_pressed()

        if not self.moving:
            if keys[pygame.K_RIGHT] and self.currentLevel < self.maxLevel:
                self.moveDirection = self.getMovementData(True)
                self.currentLevel += 1
                self.moving = True
            elif keys[pygame.K_LEFT] and self.currentLevel > 0:
                self.moveDirection = self.getMovementData(False)
                self.currentLevel -= 1
                self.moving = True
            elif keys[pygame.K_SPACE]:
                self.createLevel(self.currentLevel)
    
    def updateIconPosition(self):
        if self.moving and self.moveDirection:
            self.icon.sprite.pos += self.moveDirection * self.speed
            targetNode = self.nodes.sprites()[self.currentLevel]

            if targetNode.hitbox.collidepoint(self.icon.sprite.pos):
                self.moving = False
                self.moveDirection= pygame.math.Vector2(0,0)

    def getMovementData(self, direction):
        start = pygame.math.Vector2(self.nodes.sprites()[self.currentLevel].rect.center)
        if direction:
            end = pygame.math.Vector2(self.nodes.sprites()[self.currentLevel + 1].rect.center)
        else:
            end = pygame.math.Vector2(self.nodes.sprites()[self.currentLevel - 1].rect.center)

        final = (end - start).normalize()
        return (final)
    
    def run(self):
        self.input()
        self.updateIconPosition()
        self.icon.update()

        self.background.draw(self.displaySurface)
        self.drawPaths()
        self.nodes.draw(self.displaySurface)
        self.nodes.update()
        self.icon.draw(self.displaySurface)

