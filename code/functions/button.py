import pygame

class Button():
  def __init__(self, x, y, Img, scale):
    self.image = pygame.transform.scale_by(Img, scale)
    self.rect = self.image.get_rect(topleft = (x,y))
    self.clicked = False

  def draw(self, surface):
    action = False

    mousePos = pygame.mouse.get_pos() #Obtain mouse position

    if self.rect.collidepoint(mousePos): #Detect if cursor and button are lying in the same coordinates
      if pygame.mouse.get_pressed()[0] and self.clicked == False: #Detect if left click is pressed
        self.clicked = True
        action = True
      elif pygame.mouse.get_pressed()[0] == False: #Detect if left click is released or not pressed
        self.clicked = False
        action = False

    surface.blit(self.image, (self.rect.x, self.rect.y)) #Draw button onto screen

    return action
