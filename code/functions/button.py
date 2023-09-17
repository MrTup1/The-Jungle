import pygame

class Button():
  def __init__(self, x, y, Img, scale):
    self.image = pygame.transform.scale_by(Img, scale)
    self.rect = self.image.get_rect(topleft = (x,y))
    self.clicked = False

  def draw(self, surface):
    action = False

    mousePos = pygame.mouse.get_pos()

    if self.rect.collidepoint(mousePos):
      if pygame.mouse.get_pressed()[0] and self.clicked == False:
        self.clicked = True
        action = True
      elif pygame.mouse.get_pressed()[0] == False:
        self.clicked = False
        action = False

    surface.blit(self.image, (self.rect.x, self.rect.y))

    return action