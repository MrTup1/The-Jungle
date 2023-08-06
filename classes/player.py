import pygame
import time
from settings import *
from functions.support import importFolder

class Player(pygame.sprite.Sprite):
	def __init__(self, pos):
		super().__init__()
		self.importCharacterAssets()
		self.frameIndex = 0
		self.animationSpeed = 0.15
		self.image = self.animations['idle'][self.frameIndex]
		self.rect = self.image.get_rect(topleft = pos)
		self.landed = False

		#movement
		self.direction = pygame.math.Vector2(0,0)
		self.speed = 8
		self.gravity = 0.8
		self.jumpSpeed = -18

	def importCharacterAssets(self):
		characterPath = './graphics/character/'
		self.animations = {"idle" :[], "run":[], "jump":[], "fall":[]}

		for animation in self.animations.keys():
			fullPath = characterPath + animation
			self.animations[animation] = importFolder(fullPath)

	def animate(self):
		animation = self.animations["run"]

		self.frameIndex += self.animationSpeed
		if self.frameIndex >= len(animation):
			self.frameIndex = 0
		
		self.image = animation[int(self.frameIndex)]
			
	def get_input(self):
		keys = pygame.key.get_pressed()
		if keys[pygame.K_RIGHT]:
			self.direction.x = 1
		elif keys[pygame.K_LEFT]:
			self.direction.x = -1
		else:
			self.direction.x = 0

		if keys[pygame.K_z]:
			if (self.direction.y == 0):
				self.jump()

	def applyGravity(self):
		self.direction.y += self.gravity
		self.rect.y += self.direction.y
	
	def jump(self):
		self.direction.y = self.jumpSpeed

	def update(self):
		self.get_input()
		self.animate()