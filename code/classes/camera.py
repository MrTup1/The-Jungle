import pygame
vec = pygame.math.Vector2
from settings import *
from functions.background import Background

class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.displaySurface = pygame.display.get_surface()
        self.offset = pygame.math.Vector2(0,0)

        self.cameraBorders = {'left': 250, 'right': 250, 'top': 100, 'bottom': 50}
        l = self.cameraBorders['left']
        t = self.cameraBorders['top'] 
        w = screenWidth - (self.cameraBorders['left'] + self.cameraBorders['right'])
        h = 250 #250 pixels ideal
        self.cameraRect = pygame.Rect(l,t,w,h)
        self.background = Background()
        self.halfW = screenWidth // 2
        self.halfH = screenHeight //2


    
    def boxCamera(self, target):
        player = target.sprite
        if player.rect.left < self.cameraRect.left:
            self.cameraRect.left = player.rect.left
        if player.rect.right > self.cameraRect.right:
            self.cameraRect.right = player.rect.right
        
        print(player.rect.top, self.cameraRect.top, self.cameraRect.bottom)
        if player.rect.top < self.cameraRect.top:
            self.cameraRect.top = player.rect.top

        if player.rect.bottom > self.cameraRect.bottom:
            self.cameraRect.bottom = player.rect.bottom    

        self.offset.x = self.cameraRect.left - self.cameraBorders['left']
        self.offset.y = self.cameraRect.top - self.cameraBorders['right'] 

    def customDraw(self, player):
        self.boxCamera(player)
        self.background.draw(self.displaySurface, self.offset.x)

        for sprite in self.sprites():
            offsetPos = sprite.rect.topleft - self.offset
            self.displaySurface.blit(sprite.image, offsetPos)
    