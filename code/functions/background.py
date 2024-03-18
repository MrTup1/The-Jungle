import pygame
import time
import math
import random
from settings import *

class Background: #Displays parallax background in game
  def __init__(self):
      self.bgwidth = 0
      self.bgImages = [] #List contains all image surfaces for the background
      self.speed = 0

      for i in range(1,6): #6 layers for background
        bgImage = pygame.image.load(f"./graphics/decoration/background/plx-{i}.png").convert_alpha()
        bgImage = pygame.transform.scale(bgImage, (screenWidth, screenHeight)) #Scale each image to screen size
        self.bgwidth = bgImage.get_width() 
        self.bgImages.append(bgImage)
  
  def draw(self, surface, bgScroll):
    bgScroll = bgScroll + 1000

    for j in range(-2, 100): #Draw 100 backgrounds towards the right
      self.speed = 1
      for i in self.bgImages: #Apply to every background layer
        #Logic for parallax background. 1st draw 100 images directly next to each other for each image. Last image (towards the back) moves faster than the front layer, as it has higher self.speed value
        surface.blit(i, ((j * self.bgwidth) - bgScroll * self.speed, 0)) 
        self.speed += 0.05
