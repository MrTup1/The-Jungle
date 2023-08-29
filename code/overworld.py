import pygame
from game_data import levels

class Node(pygame.sprite.Sprite):
    def __init__(self, pos, status):
        super().__init__()
        self.image = pygame.Surface((100, 80))
        if status == 'available':
            self.image.fill("GREEN")
        else:
            self.image.fill("RED")     

        self.rect = self.image.get_rect(center = pos)

class Icon(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.Surface((20,20))
        self.image.fill('BLUE')
        self.rect = self.image.get_rect(center = pos)

class Overworld:
    def __init__(self, startLevel, maxLevel, surface):
        self.displaySurface = surface
        self.maxLevel = maxLevel
        self.currentLevel = startLevel
        self.moving = False

        self.moveDirection = pygame.math.Vector2(0,0)
        self.speed = 8

        self.setupNodes()
        self.setupIcon()

    def setupNodes(self):
        self.nodes = pygame.sprite.Group()

        for index, nodeData in enumerate(levels.values()):
            if index <= self.maxLevel:             
              nodeSprite = Node(nodeData['nodePos'], 'available')
            else: 
              nodeSprite = Node(nodeData['nodePos'], 'locked')
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
        pygame.draw.lines(self.displaySurface, 'RED', False, pointList, 6)

    def input(self):
        keys = pygame.key.get_pressed()

        if not self.moving:
            if keys[pygame.K_RIGHT] and self.currentLevel <= self.maxLevel:
                self.moveDirection = self.getMovementData()
                self.currentLevel += 1
                self.moving = True
                print(self.moveDirection)
            elif keys[pygame.K_LEFT] and self.currentLevel > 0:
                self.currentLevel -= 1
                self.moving = True
    
    def updateIconPosition(self):
        self.icon.sprite.rect.center += self.moveDirection * self.speed

    def getMovementData(self):
        start = pygame.math.Vector2(self.nodes.sprites()[self.currentLevel].rect.center)
        end = pygame.math.Vector2(self.nodes.sprites()[self.currentLevel + 1].rect.center)
        final = (end - start).normalize()
 
        return (final)

    def run(self):
        self.input()
        self.updateIconPosition()
        self.drawPaths()
        self.nodes.draw(self.displaySurface)
        self.icon.draw(self.displaySurface)

