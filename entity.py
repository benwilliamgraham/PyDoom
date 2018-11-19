import math
import pygame
import random

from ctypes import *
from mathematics import *
from OpenGL.GL import *
from OpenGL.GLU import *
from pygame.locals import *
from texture import *

gravity = -0.01

class Entity(object):
	def __init__(self, position):
		self.position = position

	def draw(self):
		pass

	def update(self, world, player):
		pass

class Player(Entity):
	def __init__(self, position, rotation):
		super().__init__(position)
		self.rotation = rotation
		self.velocity = Vec3(0, 0, 0)
		rad = Vec3(0.25, 0.45, 0.25)
		self.faceMesh = (
			Vec3(-rad.x, -rad.y, -rad.z),
			Vec3(-rad.x, -rad.y, rad.z),
			Vec3(-rad.x, rad.y, -rad.z),
			Vec3(-rad.x, rad.y, rad.z),
			Vec3(rad.x, -rad.y, -rad.z),
			Vec3(rad.x, -rad.y, rad.z),
			Vec3(rad.x, rad.y, -rad.z),
			Vec3(rad.x, rad.y, rad.z),
		)

	def checkCollision(self, world, delta):
		for point in self.faceMesh:
			if world.checkCollision()

	def control(self, world, entities, keys, display):
		deltaPos = Vec3(0, 0, 0)
		deltaRot = Vec3(0, 0, 0)
		if keys[K_w]:
			deltaPos.z += 1
		elif keys[K_s]:
			deltaPos.z -= 1
		if keys[K_d]:
			deltaPos.x += 1
		elif keys[K_a]:
			deltaPos.x -= 1
		
		deltaMouse = pygame.mouse.get_pos()
		deltaRot.y = deltaMouse[0] - display[0] // 2
		deltaRot.x = deltaMouse[1] - display[1] // 2
		pygame.mouse.set_pos(display[0] // 2, display[1] // 2)
		pygame.mouse.set_visible(False)

		self.rotation += deltaRot * 0.23
		self.rotation.x = max(min(self.rotation.x, 30), -30)
		dx = (deltaPos.x * math.cos(self.rotation.y * 3.14 / 180) + deltaPos.z * math.sin(self.rotation.y * 3.14 / 180)) * 0.1
		dz = (deltaPos.x * math.sin(self.rotation.y * 3.14 / 180) - deltaPos.z * math.cos(self.rotation.y * 3.14 / 180)) * 0.1

		self.velocity.y += gravity

		if self.checkCollision(world, Vec3(0, self.velocity.y, 0)):
			self.velocity.y *= -0.4

		self.position.y += self.velocity.y
		

class Particle(Entity):
	def __init__(self, position, velocity):
		super().__init__(position)

class Door(Entity):
	def __init__(self, position):
		super().__init__(position)

class Slime(Entity):
	def __init__(self, position):
		super().__init__(position)