import pygame
import time
import math
import random
from settings import *

class Background:
  def __init__(self):
      self.bgwidth = 0
      self.bgImages = [] 
      self.speed = 0

      for i in range(1,6):
        bgImage = pygame.image.load(f"./graphics/decoration/background/plx-{i}.png").convert_alpha()
        bgImage = pygame.transform.scale(bgImage, (screenWidth, screenHeight))
        self.bgwidth = bgImage.get_width()
        self.bgImages.append(bgImage)
  
  def draw(self, surface, bgScroll):
    bgScroll = bgScroll + 400
    for j in range(-2, 100):
      self.speed = 1
      for i in self.bgImages:
        surface.blit(i, ((j * self.bgwidth) - bgScroll * self.speed, 0))
        self.speed += 0.05

class OverworldBackground(Background):
    def __init__(self):
       super().__init__()
    
    def draw(self, surface):
      for i in self.bgImages:
        surface.blit(i, (0, 0))
        self.speed += 0.05