import pygame
vec = pygame.math.Vector2
from settings import *

class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.displaySurface = pygame.display.get_surface()
        self.offset = pygame.math.Vector2(0, 350)

        self.cameraBorders = {'left': 150, 'right': 150, 'top': 50, 'bottom': 50}
        l = self.cameraBorders['left']
        t = self.cameraBorders['top']
        w = screenWidth - self.cameraBorders['left'] - self.cameraBorders['right']
        h = screenHeight - self.cameraBorders['top'] - self.cameraBorders['bottom']
        self.cameraRect = pygame.Rect(l,t,w,h)


    
    def boxCamera(self, target):
        player = target.sprite
        if player.rect.left < self.cameraRect.left:
            self.cameraRect.left = player.rect.left
        if player.rect.right > self.cameraRect.right:
            self.cameraRect.right = player.rect.right

        self.offset.x = self.cameraRect.left - self.cameraBorders['left']      

    def customDraw(self, player):
        self.boxCamera(player)

        for sprite in self.sprites():
            offsetPos = sprite.rect.topleft - self.offset
            self.displaySurface.blit(sprite.image, offsetPos)