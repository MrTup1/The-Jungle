import pygame
import time
from settings import *
from functions.support import importFolder

class Player(pygame.sprite.Sprite):
	def __init__(self, pos, group):
		super().__init__(group)
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
		self.time = 0
		self.releasedJump = False

		#movement
		self.direction = pygame.math.Vector2(0,0)
		self.speed = 4
		self.gravity = 0.8
		self.jumpSpeed = -10

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

		#draws image on where actual rect is (stick to ground)
		if self.onGround and self.onRight:
			self.rect = self.image.get_rect(midbottom = self.rect.midbottom)
		elif self.onGround and self.onLeft:
			self.rect = self.image.get_rect(bottomleft = self.rect.bottomleft)
		elif self.onGround:
			self.rect = self.image.get_rect(midbottom = self.rect.midbottom)
		elif self.onCeiling and self.onRight:
			self.rect = self.image.get_rect(topright = self.rect.topright)
		elif self.onCeiling and self.onLeft:
			self.rect = self.image.get_rect(topleft = self.rect.topleft)
		elif self.onCeiling:
			self.rect = self.image.get_rect(midtop = self.rect.midtop)
		
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
			#if (self.direction.y == 0) and self.onCeiling == False:
			self.time += 1
			if self.time < 13 and self.onCeiling == False and self.releasedJump == False:
					self.jump()
		elif keys[pygame.K_z] == False:
				self.time = 0
				self.releasedJump = True

	def getStatus(self):
		if self.direction.y < 0:
			self.status = "jump"
		elif self.direction.y > 0.8:
			self.status = "fall"
		else:
			if self.direction.x != 0:
				self.status = "run"
				self.releasedJump = False
			else:
				self.status = "idle"
				self.releasedJump = False
		

	def applyGravity(self):
		self.direction.y += self.gravity
		self.rect.y += self.direction.y
	
	def jump(self):
		self.direction.y = self.jumpSpeed

	def update(self):
		self.get_input()
		self.getStatus()
		self.animate()