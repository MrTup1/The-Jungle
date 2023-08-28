import pygame
from game_data import levels

class Node(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.Surface((100, 80))
        self.image.fill("GREEN")
        self.rect = self.image.get_rect(center = pos)

class Overworld:
    def __init__(self, startLevel, maxLevel, surface):
        self.displaySurface = surface
        self.maxLevel = maxLevel
        self.currentLevel = startLevel

    def setupNodes(self):
        self.nodes = pygame.sprite.Group()
        for nodeData in levels.values():
            nodeSprite = Node(nodeData['nodePos'])
            self.nodes.add(nodeSprite)
    
    def run(self):
        self.nodes.draw(self.displaySurface)