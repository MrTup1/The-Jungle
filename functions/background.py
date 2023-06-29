import pygame
import time
import math
import random
from settings import *

def draw_bg(bgScroll, i, backgroundImg_width):
	screen.blit(backgroundImg, (i* backgroundImg_width + bgScroll, 0))