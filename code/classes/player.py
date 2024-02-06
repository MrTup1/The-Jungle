import pygame
import time
from settings import *
from functions.support import importFolder
from math import sin
import numpy as np

class Player(pygame.sprite.Sprite):
	def __init__(self, pos, group, changeHealth, paused, currentLevel):
		super().__init__(group)
		self.importCharacterAssets()
		self.frameIndex = 0
		self.animationSpeed = 0.15
		self.image = self.animations['idle'][self.frameIndex]
		self.rect = self.image.get_rect(topleft = pos)
		self.rect.height = 64
		self.rect.width = 32
		self.collisionRect = pygame.Rect(self.rect.topleft , (24 , 50))
		self.currentLevel = currentLevel

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
		self.finalDashed = False
		self.unlockedDash = False
		self.unlockedDouble = False

		#movement
		self.direction = pygame.math.Vector2(0,0)
		self.speed = 4
		self.gravity = 1.4
		self.acceleration = 0.2
		self.jumpSpeed = -9
		self.jumped = False
		self.doubleJumped = False
		self.maxJumps = 2
		self.jumpsRemaining = 2

		self.changeHealth = changeHealth
		self.invincible = False
		self.inivincibleDuration = 400
		self.hurtTime = 0
		self.dashedTime = 1020
		self.dashCooldown = 250
		self.dashCounter = 0

		#pause
		self.pausedDirection = 0
		self.pausedCooldown = 0.15
		self.paused = paused
		self.time1 = 0
		self.time2 = 0

		#loading
		self.createTime = time.time()
		self.createWait = 0.25

		self.checkUnlocked()

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

	def checkUnlocked(self):
		if self.currentLevel > 1:
			self.unlockedDash = True
		if self.currentLevel > 2:
			self.unlockedDouble = True
	
	def get_input(self):
		currentTime = time.time() #Get new time every 60th of a second
		keys = pygame.key.get_pressed()
		if currentTime - self.createTime >= self.createWait: #Check if time elapsed is higher than wait cooldown (250ms)
			if keys[pygame.K_RIGHT]:
				self.accelerate(1)
				self.facing = "right"
			elif keys[pygame.K_LEFT]:
				self.accelerate(-1)
				self.facing = "left"
			else:
				self.direction.x = 0

			if self.unlockedDouble: #If unlocked double jump
				if keys[pygame.K_z]: #JUMP
					self.time += 1
					
					if self.jumpsRemaining > 0: #Actual movement of player
						if self.time < 16 and self.onCeiling == False:
								self.jump()

					if not self.jumped: #If player has jumped 1st time
						self.jumped = True 
						self.jumpsRemaining -= 1 

					if not self.doubleJumped and self.jumped and self.releasedJump == True: #Check if first jump is completed
						self.doubleJumped = True	

				elif keys[pygame.K_z] == False:
						self.time = 0
						if self.jumped:
							self.releasedJump = True #After 1st release of key from jump
						if self.doubleJumped:  #After 2nd release of key from jump
							self.jumpsRemaining -= 1 
			else:	#Jump when double jump is still locked			
				if keys[pygame.K_z]:
					self.time += 1
					if self.time < 16 and self.onCeiling == False and self.releasedJump == False:
							self.jump()
				elif keys[pygame.K_z] == False:
						self.time = 0
						self.releasedJump = True
		
			if self.unlockedDash:
				if keys[pygame.K_c] and self.finalDashed == False: #DASH
					self.dashed = True
				
				if self.dashed == True and self.finalDashed == False:
					if self.facing == "right":
						self.dashFunction(1)
					if self.facing == "left":
						self.dashFunction(-1)


	def getStatus(self):
		if self.direction.y < 0:
			self.status = "jump"
		elif self.direction.y > 0.8 and self.releasedJump == True:
			self.status = "fall"
		elif self.onGround == True:
			#Reset attributes
			self.jumped = False
			self.doubleJumped = False
			self.jumpsRemaining = self.maxJumps
			
			if self.finalDashed:
				currentTime = pygame.time.get_ticks()
				if currentTime - self.dashedTime >= self.dashCooldown:
					self.dashed = False
					self.finalDashed = False
					self.dashCounter = 0
			if self.direction.x != 0:
				self.status = "run"
			else:
				self.status = "idle"
		
	def getDamage(self):
		if not self.invincible:
			self.changeHealth(-1) 
			self.invincible = True
			self.hurtTime = pygame.time.get_ticks()\

	def dashFunction(self, direction):
		if self.dashed == True and self.dashCounter < 6:
			self.dashCounter +=1
			self.dash(direction)
			if self.dashCounter > 5: 
				self.finalDashed = True
				self.dashedTime = pygame.time.get_ticks()

	def dash(self, direction):
		if self.paused == False:
			self.direction.y = 0
			self.direction.x = 5 * direction
	

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


	def update(self):
		self.get_input()
		self.getStatus()
		self.animate()
		self.inivincibleTime()
		self.flicker()