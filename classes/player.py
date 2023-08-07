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

		#player status
		self.status = "idle"
		self.facing = "right"
		self.onGround = False
		self.onCeiling = False
		self.onLeft = False
		self.onRight = False

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
		animation = self.animations[self.status]

		self.frameIndex += self.animationSpeed
		if self.frameIndex >= len(animation):
			self.frameIndex = 0

		image = animation[int(self.frameIndex)]
		if self.facing == "right":
			self.image = image
		else:
			flippedImg = pygame.transform.flip(image, True, False)
			self.image = flippedImg
		
	def get_input(self):
		keys = pygame.key.get_pressed()
		if keys[pygame.K_RIGHT]:
			self.direction.x = 1
			self.facing = "right"
		elif keys[pygame.K_LEFT]:
			self.direction.x = -1
			self.facing = "left"
		else:
			self.direction.x = 0

		if keys[pygame.K_z]:
			if (self.direction.y == 0) and self.onCeiling == False:
				self.jump()

	def getStatus(self):
		if self.direction.y < 0:
			self.status = "jump"
		elif self.direction.y > 0.8:
			self.status = "fall"
		else:
			if self.direction.x != 0:
				self.status = "run"
			else:
				self.status = "idle"
		

	def applyGravity(self):
		self.direction.y += self.gravity
		self.rect.y += self.direction.y
	
	def jump(self):
		self.direction.y = self.jumpSpeed

	def update(self):
		self.get_input()
		self.getStatus()
		self.animate()