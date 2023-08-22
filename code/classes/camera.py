import pygame
vec = pygame.math.Vector2

class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.displaySurface = pygame.display.get_surface()
    
    def customDraw(self):
        for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
            self.displaySurface.blit(sprite.image, sprite.rect)
            
