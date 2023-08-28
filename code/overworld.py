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

    def run(self):
        self.drawPaths()
        self.nodes.draw(self.displaySurface)
        self.icon.draw(self.displaySurface)
