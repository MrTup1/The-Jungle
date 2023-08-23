import pygame
from classes.tile import AnimatedTile
from random import randint

class Opossum(AnimatedTile):
    def __init__(self, size, x, y, group):
        super().__init__(size, x, y, './graphics/opossum', group)
        offset = 10
        offset_y = y - offset
        self.rect.topleft = (x, offset_y)
        self.speed = randint(3, 5)

    def move(self):
        self.rect.x += self.speed
    
    def reverseImage(self):
        if self.speed > 0:
            self.image = pygame.transform.flip(self.image, True, False)

    def reverse(self):
        self.speed = self.speed * -1
        
    def update(self):
        self.animate()
        self.reverseImage()
        self.move()