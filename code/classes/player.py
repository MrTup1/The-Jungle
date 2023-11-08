import pygame
import time
from settings import *
from functions.support import importFolder
from math import sin
import numpy as np

class Player(pygame.sprite.Sprite):
	def __init__(self, pos, group, changeHealth):
		super().__init__(group)
		self.importCharacterAssets()
		self.frameIndex = 0
		self.animationSpeed = 0.15
		self.image = self.animations['idle'][self.frameIndex]
		self.rect = self.image.get_rect(topleft = pos)
		self.rect.height = 64
		self.rect.width = 32
		self.collisionRect = pygame.Rect(self.rect.topleft , (24 , 50))

		#player status
		self.status = "idle"
		self.facing = "right"
		self.onGround = False
		self.onCeiling = False
		self.onLeft = False
		self.onRight = False
		self.time = 0
		self.releasedJump = False
		self.dashed = False

		#movement
		self.direction = pygame.math.Vector2(0,0)
		self.speed = 4
		self.gravity = 0.8
		self.acceleration = 0.2
		self.jumpSpeed = -9

		self.changeHealth = changeHealth
		self.invincible = False
		self.inivincibleDuration = 400
		self.hurtTime = 0
		self.dashedTime = 1020
		self.dashCooldown = 500
		self.dashCounter = 0

		#pause
		self.pausedDirection = 0
		self.paused = False
		self.time1 = 0
		self.time2 = 0

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
			self.rect.bottomleft = self.collisionRect.bottomleft
		else:
			flippedImg = pygame.transform.flip(image, True, False)
			self.image = flippedImg
			self.rect.bottomright = self.collisionRect.bottomright

		if self.invincible:
			alpha = self.flicker()
			self.image.set_alpha(alpha)
		else:
			self.image.set_alpha(255)

		
	def get_input(self):
		keys = pygame.key.get_pressed()
		if self.paused == False:
			if keys[pygame.K_RIGHT]:
				self.accelerate(1)
				self.facing = "right"
			elif keys[pygame.K_LEFT]:
				self.accelerate(-1)
				self.facing = "left"
			else:
				self.direction.x = 0

		if keys[pygame.K_z]:
			self.time += 1
			if self.time < 14 and self.onCeiling == False and self.releasedJump == False:
					self.jump()
		elif keys[pygame.K_z] == False:
				self.time = 0
				self.releasedJump = True
		
		if keys[pygame.K_c] and self.dashed == False:
			if self.facing == "left":
				self.dash(-1)
			elif self.facing == "right":
				self.dash(1)
			self.dashCounter +=1
			if self.dashCounter > 10:
				self.dashed = True
				self.dashedTime = pygame.time.get_ticks()
		
		if keys[pygame.K_ESCAPE]:
			if self.paused == True: #Paused State
				self.time2 = time.time()
				if (self.time2 - self.time1 >= 0.5):
					self.time2 = time.time()
					self.direction.x = 0
					self.direction.y = 0
					self.paused = False
			else:	#Game State
				self.time1 = time.time()
				if (self.time1 - self.time2 >= 0.5):
					self.pausedDirectionX = self.direction.x
					self.pausedDirectionY = self.direction.y
					self.direction.y = 0
					self.direction.x = 0
					self.paused = True


	def getStatus(self):
		if self.direction.y < 0:
			self.status = "jump"
		elif self.direction.y > 0.8 and self.releasedJump == True:
			self.status = "fall"
		elif self.onGround == True:
			if self.dashed:
				currentTime = pygame.time.get_ticks()
				if currentTime - self.dashedTime >= self.dashCooldown:
					self.dashed = False
					self.dashCounter = 0
			if self.direction.x != 0:
				self.status = "run"
			else:
				self.status = "idle"
		
	def getDamage(self):
		if not self.invincible:
			self.changeHealth(-1) 
			self.invincible = True
			self.hurtTime = pygame.time.get_ticks()

	def inivincibleTime(self):
		if self.invincible:
			currentTime = pygame.time.get_ticks()
			if currentTime - self.hurtTime >= self.inivincibleDuration: 
				self.invincible = False

	def flicker(self):
		value = sin(pygame.time.get_ticks())
		if value >= 0: return 0
		else: return 255

	def applyGravity(self):
		if self.paused == False:
			self.direction.y += self.gravity
			self.collisionRect.y += self.direction.y
	
	def jump(self):
		self.direction.y = self.jumpSpeed
	
	
	def accelerate(self, direction):
		if self.direction.x + self.acceleration * direction <= 1.25 and direction == 1 or self.direction.x + self.acceleration * direction >= -1.25 and direction == -1:
			self.direction.x += self.acceleration * direction
			self.collisionRect.x += self.direction.x *direction
		else:
			if direction == 1:
				self.direction.x = 1.25
			else: 
				self.direction.x = -1.25

	def dash(self, direction):
		if self.paused == False:
			self.direction.y = 0
			self.direction.x = 5 * direction

	def update(self):
		self.get_input()
		self.getStatus()
		self.animate()
		self.inivincibleTime()
		self.flicker()